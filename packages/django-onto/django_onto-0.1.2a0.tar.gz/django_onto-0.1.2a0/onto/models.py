import logging
from typing import Any
from django.db import models
from django.db import transaction
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.utils import timezone
from .utils import clean, get_entity_pk
#from django.contrib.postgres.indexes import GinIndex

logger = logging.getLogger(__name__)

class XAttrsMixin(models.Model):
    """
    Adds an `xattrs` JSONField to the model, as well as supporting methods.

    Make sure to inherit XAttrsMixin.QuerySet into the model's Manager to gain access to the custom methods like `xfilter`.
    """
    class Meta:
        abstract = True

    class QuerySet(models.QuerySet):
        def xfilter(self, **filters):
            """
            Include only objects with the specified extended attribute (`xattrs`).
            """
            return self.filter(**{f"xattrs__{query}":value for query,value in filters.items()})

    xattrs = models.JSONField(
        "extended attributes",
        blank=True,
        default=dict,
        help_text="Arbitrary JSON attributes, e.g. tags, to attach to this object."
    )

    def xget(self, key, default=None):
        """
        Get the object's `xattrs` value by `key`, or `default` if it doesn't exist.
        """
        key = clean(key)
        return self.xattrs.get(key, default)

    def xset(self, key, value, commit=True):
        """
        Set the `key`:`value:` pair on the `xattrs` of the object.
        """
        key = clean(key)
        self.xattrs[key] = value
        if commit:
            self.save(update_fields=["xattrs"])

    def xdel(self, key, commit=True) -> None:
        """
        Remove the `key` from the `xattrs` of the object.
        """
        key = clean(key)
        try:
            del self.xattrs[key]
            if commit:
                self.save(update_fields=["xattrs"])
        except KeyError:
            pass

    def xelem_add(self, key, *values, commit=True):
        """
        Attempt to add each of `values` to the collection at `key`.

        If `key` does not exist, create it.

        If `key` exists but is not a list, raise a ValueError.
        """
        elements = self.xget(key)
        if not elements:
            elements = values
        elif not isinstance(elements, list):
            raise ValueError(f"xattrs[key] exists, but it is not a list and cannot be added to!")
        else:
            for value in values:
                if value not in elements:
                    elements.append(value)
        return self.xset(key, elements, commit=commit)

    def xelem_del(self, key, *values, commit=True):
        """
        Attempt to remove each of `values` from the collection at `key`.
        """
        elements = self.xget(key)
        if not elements:
            return
        elif not isinstance(elements, list):
            raise ValueError(f"xattrs[key] exists, but it is not a list and cannot be deleted from!")
        else:
            for value in values:
                if value in elements:
                    elements.remove(value)
        return self.xset(key, elements, commit=commit)

class Entity(XAttrsMixin, models.Model):
    """
    The central model of Onto, the Entity table contains a record for each record of every `EntityModel` subclass.

    Entities should NOT be created directly; they are automatically created whenever a new instance of an `EntityModel` subclass is created.
    """
    class Meta:
        verbose_name_plural = "entities"
#        indexes = [
#            GinIndex(fields=['xattrs']),
#            ]  # TODO Allow users to declare deeper indexes against xattrs

    class ArchiveManager(models.Manager):
        pass

    class Manager(ArchiveManager):
        def get_queryset(self):
            return super().get_queryset().exclude(archived_time__isnull=False)

        def from_object(self, obj) -> "Entity":
            """
            Return the primary Entity associated with any object, using its `entity_pk_field` attribute.

            EntityModel subclasses have this attribute by default, other classes must define it explicitly or this method will fail.
            """
            if isinstance(obj, Entity):
                return obj

            return self.get(pk=get_entity_pk(obj))

    class QuerySet(models.QuerySet):
        def archive(self):
            for entity in self:
                entity.archive()

        def restore(self):
            for entity in self:
                entity.restore()

        def within(self, domain):
            """
            Set the scope of the QuerySet to a particular Domain, and filter out entities that don't belong to it.

            Methods that interact with xattrs will then use the corresponding Membership xattrs instead of global Entity xattrs.

            In the below example, the first `xfilter` filters based on global Entity xattrs, while the latter xfilters are based solely on xattrs of Memberships to the respective domains.
            >>> Entity.objects.xfilter(flags__contains="valid") \
                    .within(acme).xfilter(roles__contains="accountant") \
                    .within("acme.accounting").xfilter(team="red")
            """
            if isinstance(domain, str):
                domain = Domain.objects.get(name=domain)
            self.query._onto_domain = domain  # self.query.__dict__ is copied through, but self.__dict__ is not.
            return self.filter(domains=domain)

        def xfilter(self, **filters):
            """
            Include only entities with the specified extended attribute (`xattrs`). If chained after `.within(domain)`, filter the `xattrs` of the associated Memberships instead.
            """
            if domain := getattr(self.query, "_onto_domain", None):
                return self.filter(pk__in=domain.memberships.xfilter(**filters).values("entity_id"))

            return self.filter(**{f"xattrs__{query}":value for query,value in filters.items()})

        def as_model(self, *models: models.Model):
            """
            Returns a dictionary mapping Models to querysets of objects of that type.

            If exactly one model is specified, returns that queryset directly.

            Examples:

            >>> Entity.objects.filter(...).as_model(User)
            <QuerySet [<User: alice>, <User: bob>, ...]>

            >>> Entity.objects.filter(...).as_model(User, Region, ...)
            {
                User: <QuerySet [<User: alice>, <User: bob>, ...]>,
                Region: <QuerySet [<Region: fredonia>, ...]>,
                ...
            }
            """
            results = dict()
            models = models or {ct.model_class() for ct in ContentType.objects.filter(pk__in=self.values_list("content_type", flat=True).distinct())}
            pks = self.values("pk")
            for model in models:
                results[model] = model.objects.filter(**{f"{model.entity_pk_field}__in":pks})

            if len(models) == 1:
                return results[model]

            return results

        def all_subdomains(self):
            """
            Recursively replace all Domain entities in the QuerySet with their constituent entities.
            """
            domain_ct = ContentType.objects.get_for_model(Domain)
            subdomains = self.filter(content_type=domain_ct)
            return self.exclude(content_type=domain_ct).union(*[subdomain.object.entities.all_subdomains() for subdomain in subdomains])


    objects: Manager = Manager.from_queryset(QuerySet)()
    objects_archive: ArchiveManager = ArchiveManager.from_queryset(QuerySet)()

    entity_pk_field = "id"
    id = models.AutoField(
        primary_key=True,
    )

    content_type = models.ForeignKey(ContentType, on_delete=models.RESTRICT, editable=False)
    content_object = GenericForeignKey('content_type', 'id')

    created_time = models.DateTimeField(
        auto_now_add=True,
        help_text="When this entity and associated object were created."
    )
    updated_time = models.DateTimeField(
        auto_now=True,
        help_text="When this entity (but not *necessarily* its associated object) was last modified."
    )
    archived_time = models.DateTimeField(
        null=True,
        blank=True,
        editable=False,
        db_index=True,
        help_text="When this entity and its associated object were last archived."
    )

    xattrs = models.JSONField(
        "extended attributes",
        blank=True,
        default=dict,
        help_text="Arbitrary JSON attributes, e.g. tags."
    )
    domains = models.ManyToManyField(
        "onto.Domain",
        related_name="entities",
        blank=True,
        through='onto.Membership',
        help_text="Domains, or entity groups, that this object is a member of."
    )

    @property
    def url(self):
        """
        Return a relative link to the details page for this object.
        """
        # TODO add prefix from settings?
        return '/'.join(("", *self.content_type.natural_key(), str(self.id)))

    def archive(self):
        self.content_object.archived = True
        self.content_object.save(update_fields=["archived"])
        self.archived_time = timezone.now()
        return self.save(update_fields=["archived_time"])

    def within(self, domain) -> "Membership":
        """
        Return the entity's Membership with the Domain, if it exists.
        """
        if isinstance(domain, str):
            domain = Domain.objects.get(name=domain)
        return domain.memberships.get(entity_id=self.pk)

    def is_within(self, domain) -> bool:
        """
        Returns whether the entity is a member of the Domain.
        """
        if isinstance(domain, str):
            domain = Domain.objects.get(name=domain)
        return domain.entities.filter(pk=self.pk).exists()

    def join_domain(self, domain) -> "Membership":
        """
        Add this Entity to the specified domain, returning the Membership..
        """
        if isinstance(domain, str):
            domain = Domain.objects.get(name=domain)

        membership, created = self.memberships.get_or_create(domain=domain)
        return membership

    def leave_domain(self, domain) -> None:
        """
        Remove this Entity from the specified domain, deleting the Membership.
        """
        if isinstance(domain, str):
            domain = Domain.objects.get(name=domain)

        return self.domains.remove(domain)

    def related_objects(self, model) -> models.QuerySet:
        """
        Return a QuerySet of `model` where `model.entity_pk_field` resolves to this Entity.
        """
        return model.objects.filter(**{f"{model.entity_pk_field}":self.pk})

    def __str__(self):
        return '.'.join((*self.content_type.natural_key(), str(self.content_object)))


class EntityModel(models.Model):
    """
    Abstract class that overrides the default `id` primary key with a OneToOne field to the Entity table called `entity_id`.
    Also adds a `archived` BooleanField to allow "soft-deletion".

    This means each EntityModel represents two database records, one for the usual table, and one in the Entity table.
    This gives us the powerful ability to query all Entities at once with zero joins, even if the underlying schemas are incompatible.

    However, it does mean we must be careful with which models inherit this, so as to not pollute this precious global "namespace".
    Good candidates: Person, Location, Organization, Asset, System, Country, ~Article, etc. 
    (Entities or "business objects" that *exist* outside this database or would benefit strongly from the querying functionality.)
    Bad candidates: Event, Log, sensor reading, relationship/m2m tables, transaction record, etc.

    Otherwise, this EntityModel behaves like any other base Model subclass.
    """
    class Meta:
        abstract = True

    class QuerySet(models.QuerySet):
        @property
        def entities(self):
            """
            Return the QuerySet of corresponding Entities. This is a nested query, so could be slow for large QuerySets!
            """
            return Entity.objects_archive.filter(pk__in=self)

        def in_domain(self, domain):
            if isinstance(domain, str):
                domain = Domain.objects.get(name=domain)

            return self.filter(entity__domains=domain)

        def within(self, domain):
            """
            Set the scope of the QuerySet to a particular Domain, and filter out entities that don't belong to it.

            Methods that interact with xattrs will then use the corresponding Membership xattrs instead of global Entity xattrs.

            In the below example, the first `xfilter` filters based on global Entity xattrs, while the latter xfilters are based solely on xattrs of Memberships to the respective domains.
            >>> users.xfilter(flags__contains="valid") \
                    .within(acme).xfilter(roles__contains="accountant") \
                    .within("acme.accounting").xfilter(team="red")
            """
            if isinstance(domain, str):
                domain = Domain.objects.get(name=domain)
            self.query._onto_domain = domain  # NOTE: self.query.__dict__ is copied through, but self.__dict__ is not.
            return self.filter(entity__domains=domain)

        def xfilter(self, **filters):
            """
            Include only entities with the specified extended attribute (`xattrs`).
            """
            if domain := getattr(self.query, "_onto_domain", None):
                return self.filter(pk__in=domain.memberships.xfilter(**filters).values("entity_id"))

            return self.filter(**{f"entity__xattrs__{query}":value for query,value in filters.items()})

        def delete(self, *args, **kwargs):
            """
            Delete all objects in the QuerySet by deleting their associated Entities.
            """
            return self.entities.delete(*args, **kwargs)

        def archive(self):
            """
            "Soft-deletes" objects in the QuerySet, preventing them from showing up in the default `objects` Manager.

            Use the `objects_archive` Manager to query both archived and unarchived objects.
            """
            with transaction.atomic():
                self.entities.update(archived_time=timezone.now())
                self.update(archived=True)

        def restore(self):
            """
            Reverses the archiving i.e. "soft-deletion" of objects in the QuerySet (see `.archive()`).
            
            Note that the default `objects` Manager won't select archived objects, so this method will only be useful on the `objects_archive` Manager.
            """
            with transaction.atomic():
                self.update(archived=False)
                self.entities.update(archived_time=None)


    class ArchiveManager(models.Manager.from_queryset(QuerySet)):
        use_in_migrations = False  # Not worth the hassle/footguns

    class Manager(ArchiveManager):
        def get_queryset(self):
            return super().get_queryset().exclude(archived=True)

    objects = Manager()
    objects_archive = ArchiveManager()

    entity_pk_field = "entity_id"
    entity = models.OneToOneField(
        Entity,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name="+",
        editable=False,
    )
    archived = models.BooleanField(
        default=False,
        editable=False,
        db_index=True,
        help_text="True indicates the object has been archived and won't appear in most queries."
    )

    @property
    def content_type(self):
        # This is cached by default.
        return ContentType.objects.get_for_model(type(self))

    def within(self, domain):
        """
        Return the object's Membership with the Domain, raising an exception if it does not exist.
        """
        if isinstance(domain, str):
            domain = Domain.objects.get(name=domain)
        return domain.memberships.get(entity_id=self.pk)

    def is_within(self, domain):
        """
        Returns whether the object is a member of the Domain.
        """
        if isinstance(domain, str):
            domain = Domain.objects.get(name=domain)
        return domain.entities.filter(pk=self.pk).exists()

    def join_domain(self, domain):
        """Add this entity to the specified domain."""
        return self.entity.join_domain(domain)

    def leave_domain(self, domain):
        """Remove this entity from the specified domain, deleting the Membership."""
        return self.entity.leave_domain(domain)

    def xget(self, key, default=None) -> Any:
        """Get the associated Entity's `xattrs` value by `key`, or `default` if it doesn't exist."""
        return self.entity.xget(key, default=default)

    def xset(self, key, value, commit=True) -> None:
        """Add the `key`:`value:` pair to the `xattrs` of the associated Entity."""
        return self.entity.xset(key, value, commit=commit)

    def xdel(self, key, commit=True) -> None:
        """Remove the `key` from the `xattrs` of the associated Entity."""
        return self.entity.xdel(key, commit=commit)

    def xelem_add(self, key, *values, commit=True):
        """Attempt to add each of `values` to the collection at `key`. If `key` does not exist, create it. If `key` exists but is not a list, raise a ValueError."""
        return self.entity.xelem_add(key, *values, commit=commit)

    def xelem_del(self, key, *values, commit=True):
        """Attempt to remove each of `values` from the collection at `key`."""
        return self.entity.xelem_del(key, *values, commit=commit)

    def save(self, *args, **kwargs):
        with transaction.atomic():
            created = self._state.adding
            if created:
                if not hasattr(self, "entity"):
                    ct = ContentType.objects.get_for_model(self.__class__)
                    self.entity = Entity.objects.create(content_type=ct)
            result = super().save(*args, **kwargs)
            if created:
                self.refresh_from_db()  # need this to make sure that (self.entity.content_object == self) right away
            return result

    def delete(self, *args, **kwargs):
        """
        Permanently deletes the object by deleting its associated Entity.
        """
        return self.entity.delete(*args, **kwargs)

    def archive(self):
        """
        Soft-deletes the object by marking it `archived` and preventing the default `objects` Manager from accessing it.
        """
        return self.entity.archive()

    def restore(self):
        """
        Reverses the archiving or "soft-deletion" of the object and its Entity.
        """
        return self.entity.restore()


class Domain(EntityModel):
    """
    A set of Entities, which is itself an Entity (and therefore can be added to other Domains).
    """
    class Manager(EntityModel.Manager):
        def get_by_natural_key(self, name):
            return self.get(name=name)

        def create_with_parent(self, parent: "Domain", name, ignore_exists=False):
            if not ignore_exists:
                domain = self.create(name=f"{parent.name}.{name}")
            else:
                domain, created = self.get_or_create(name=f"{parent.name}.{name}")

            domain.join_domain(parent)
            return domain

    objects = Manager()

    name = models.SlugField(unique=True, max_length=255)

    #TODO
    def xfilter_entities(self, **filters):
        return self.memberships.xfilter(**filters)

    @property
    def superdomains(self):
        return self.entity.domains.all()

    @property
    def subdomains(self):
        return self.entities.as_model(Domain)

    def has_subdomain_recursive(self, subdomain) -> bool:
        """
        Returns True if `subdomain` is a subdomain of this domain or any of its subdomains, recursively.
        """
        if subdomain == self:
            return True

        for domain in self.subdomains:
            if domain.has_subdomain_recursive(subdomain):
                return True

        return False

    def create_subdomain(self, subdomain_name, ignore_existing=False, **kwargs) -> "Domain":
        """
        Creates a new domain with the current domain's name followed by `.subdomain_name`, and joins the new subdomain to this one.

        Specify `ignore_existing=True` to join the subdomain even if it already exists.

        Example:
        >>> domain1 = Domain.objects.create(name="acme")
        >>> domain2 = domain1.create_subdomain("accounting")
        >>> domain2.name
        "acme.accounting"
        >>> domain2 in domain1.subdomains
        True
        """
        if not ignore_existing:
            subdomain = Domain.objects.create(name=f"{self.name}.{subdomain_name}", **kwargs)
        else:
            subdomain, created = Domain.objects.get_or_create(name=f"{self.name}.{subdomain_name}", **kwargs)

        subdomain.join_domain(self)
        return subdomain

    def natural_key(self):
        return (self.name,)

    def __str__(self):
        return self.name

class Membership(XAttrsMixin, models.Model):
    """
    Represents the Domain-Entity M2M relationship.

    Has its own set of `xattrs`, allowing arbitrary data to be associated with individual relationships.
    """
    class QuerySet(XAttrsMixin.QuerySet, models.QuerySet):
        @property
        def entities(self):
            return Entity.objects.filter(pk__in=self.values("entity").distinct())

        @property
        def domains(self):
            return Domain.objects.filter(pk__in=self.values("domain").distinct())

        def as_model(self, *models: models.Model, annotate_xattrs=False):
            """
            Returns a dictionary mapping Models to querysets of objects of that type, as contained in the Memberships.

            If exactly one model is specified, returns that queryset directly.

            If `annotate_xattrs` is True, annotate each object with its Membership `xattrs`; this uses a raw query for efficiency and cannot be further chained.
            """
            results = dict()
            models = models or {ct.model_class() for ct in ContentType.objects.filter(pk__in=self.values_list("content_type", flat=True).distinct())}
            for model in models:
                ct = ContentType.objects.get_for_model(model)
                matching = self.filter(entity__content_type=ct)  # Could remove the contenttype filter to remove a join at cost of larger IN, may want to profile
                if not annotate_xattrs:
                    results[model] = model.objects.filter(entity_id__in=matching.values("entity_id"))
                else:
                    results[model] = model.objects.raw(f"SELECT model.*, ms.xattrs::json FROM {model._meta.db_table} model INNER JOIN {Membership._meta.db_table} ms ON model.entity_id=ms.entity_id WHERE ms.id IN ({matching.values('id').query});")

            if len(models) == 1:
                return results[model]

            return results
        

    objects = QuerySet.as_manager()

    domain = models.ForeignKey(
        Domain,
        on_delete=models.CASCADE,
        related_name="memberships",
    )
    entity = models.ForeignKey(
        Entity,
        on_delete=models.CASCADE,
        related_name="memberships",
    )

    @property
    def object(self):
        return self.entity.content_object

    def __str__(self):
        return f"{self.entity}@{self.domain}"

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["entity", "domain"], name="%(app_label)s_%(class)s_unique")
        ]


class ContainerMixin(models.Model):
    """
    A mixin that associates the instance with a Domain (one-to-one), and adds some useful methods for interacting with that domain.

    Useful for implementing Groups, Projects, etc. that may represent various resources.

    Example:
    >>> class Project(ContainerMixin, EntityModel):
    ...     name = models.CharField(max_length=255, unique=True)
    ...     def initialize_content_domain(self):
    ...         return Domain.objects.create(name=self.name)
    ...
    >>> project = Project.objects.create(name="test")
    >>> project.add(user, roles=["viewer", "editor"])
    >>> project.contains(user)
    True
    >>> user in project.filter_contents(role__contains="editor")
    True
    """
    class Meta:
        abstract = True

    content_domain = models.OneToOneField(
        Domain,
        on_delete=models.CASCADE,
        editable=False,
        related_name="+",
        help_text="A domain representing the contents of this object."
    )

    @property
    def contents(self) -> Entity.QuerySet:
        return self.content_domain.entities

    def add(self, content: EntityModel) -> Membership:
        """
        Add `content` EntityModel to the `content_domain` of this object and return the resulting Membership.
        """
        return content.join_domain(self.content_domain)

    def member(self, content: EntityModel) -> Membership:
        """
        Return the Membership associated with `content`, if it exists, or raise an error.

        `content` can be an EntityModel subclass instance, or an entity primary key.
        """
        if not isinstance(content, EntityModel):
            return self.content_domain.memberships.get(entity_id=content)

        return content.within(self.content_domain)

    def contains(self, content: EntityModel) -> bool:
        """
        Check if the `content` EntityModel is a member of this object's `content_domain`.
        """
        return content.is_within(self.content_domain)

    def remove(self, content: EntityModel) -> None:
        """
        Remove the `content` EntityModel from this object's `content_domain`.
        """
        return content.leave_domain(self.content_domain)

    def save(self, *args, **kwargs):
        if self._state.adding:
            created = True
            self.content_domain = self.initialize_content_domain()
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)
        self.content_domain.delete()

    def members(self, **filters) -> Membership.QuerySet:
        """
        Shortcut to `xfilter` Membership xattrs (not Entity xattrs!).

        For example:
        >>> self.members(role__in={"viewer", "editor"}).as_model(User)
        <QuerySet of Users with viewer or editor role>
        """
        return self.content_domain.memberships.xfilter(**filters)

    def initialize_content_domain(self) -> Domain:
        """
        This method is called only when an instance is created, to initialize its `content_domain`.
        """
        raise NotImplementedError("You must define this method! Could be as simple as `return onto.models.Domain.objects.create(name=self.name, authorizes=False)`.")