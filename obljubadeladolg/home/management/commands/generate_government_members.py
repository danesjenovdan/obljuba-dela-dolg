from django.core.management.base import BaseCommand, CommandError
from home.models.pages import PromiseListingPage, GovernmentPage
from home.models.promise import Party, PartyMember, OrderablePartyMember

class Command(BaseCommand):
    help = 'For given mandate IDs (PromiseListingPage) create missing OrderablePartyMember objects.'

    def add_arguments(self, parser):
        parser.add_argument('mandate_ids', nargs='+', type=int)

    def handle(self, *args, **options):
        for mandate_id in options['mandate_ids']:
            try:
                mandate = PromiseListingPage.objects.get(pk=mandate_id)
            except PromiseListingPage.DoesNotExist:
                raise CommandError('Mandate with ID "%s" does not exist' % mandate_id)

            mandate_parties = Party.objects.filter(mandate=mandate)
            members = PartyMember.objects.filter(party__in=mandate_parties)

            government_page = GovernmentPage.objects.get(mandate=mandate)

            for member in members:
                try:
                    ordered_member = OrderablePartyMember.objects.get(member=member)
                except OrderablePartyMember.DoesNotExist:
                    ordered_member = OrderablePartyMember(member=member, government=government_page)
                    ordered_member.save()

            self.stdout.write(self.style.SUCCESS('Finished for mandate ID "%s"' % mandate_id))
