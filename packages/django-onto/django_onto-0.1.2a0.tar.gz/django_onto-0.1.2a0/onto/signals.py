"""
onto includes a few signals to make sure cycles don't form in the Domain graph.
"""
from django.dispatch import receiver
from django.db.models import signals
from django.contrib.contenttypes.models import ContentType
from . import models

class DomainCycleException(Exception):
    pass

def assert_no_membership_cycles(subdomain, superdomain):
    """
    Raises a `DomainCycleException` if adding `subdomain` to `superdomain` would cause a cycle in the Domain graph.
    """
    if subdomain.has_subdomain_recursive(superdomain):
        raise DomainCycleException(f"prevented a cycle from forming in the domain graph including '{subdomain}' and '{superdomain}'")

@receiver(signals.pre_save, sender=models.Membership)
def before_membership_saved(instance, **kwargs):
    """
    Prevent cycles from forming in the domain graph.
    """
    print("before_membership_save", instance)
    if instance.entity.content_type == ContentType.objects.get_for_model(models.Domain):
        return assert_no_membership_cycles(instance.object, instance.domain)

@receiver(signals.m2m_changed, sender=models.Domain.entities.through)
def before_domain_entities_m2m_changed(action, instance, pk_set, **kwargs):
    """
    Prevent cycles from forming in the domain graph.
    """
    print("before_domain_entities_m2m_changed", instance)
    if action == "pre_add":
        if isinstance(instance, models.Domain):
            superdomains = [instance]
            subdomains = models.Domain.objects.filter(pk__in=pk_set)
        else:
            superdomains = models.Domain.objects.filter(pk__in=pk_set)
            subdomains = models.Domain.objects.filter(pk=instance)

        for subdomain in subdomains:
            for superdomain in superdomains:
                assert_no_membership_cycles(subdomain, superdomain)