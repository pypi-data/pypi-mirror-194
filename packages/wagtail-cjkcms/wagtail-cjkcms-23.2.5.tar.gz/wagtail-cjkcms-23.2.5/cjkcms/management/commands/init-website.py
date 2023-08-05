from django.core.management.base import BaseCommand
from wagtail.models import Page
from django.apps import apps


class Command(BaseCommand):
    """
    # Delete the default home page generated by wagtail,
    # and replace it with a more useful page type based on CMS.
    # Unless specific class is given, use the cjkcms.WebPage
    """

    help = "Replaces the default Wagtail HomePage with a CMS page"

    def add_arguments(self, parser):
        # Named (optional) arguments
        parser.add_argument(
            "--force",
            action="store_true",
            help="Force overwrite if more than a homepage already exists",
        )

        parser.add_argument(
            "--host_name",
            action="store",
            default="localhost",
            help="Custom hostname for the new site",
        )

        parser.add_argument(
            "--site_name",
            action="store",
            default="devsite",
            help="Custom site name for the new site",
        )

        parser.add_argument(
            "--page_app",
            action="store",
            default="cjkcms",
            help="Custom app to use for the new homepage. Defaults to `cjkcms`",
        )

        parser.add_argument(
            "--page_model",
            action="store",
            default="WebPage",
            help="Custom class to use for the new homepage. Defaults to WebPage",
        )

    def handle(self, raise_error=False, *args, **options):
        # check if ok to overwrite (force == 1)
        force = options["force"]
        verbosity = options["verbosity"]
        checks = [Page.objects.count() > 2]  # root + home = 2
        page_app = options["page_app"]
        page_model = options["page_model"]
        host_name = options["host_name"]
        site_name = options["site_name"]

        if any(checks) and not force:
            # YOU SHOULD NEVER RUN THIS COMMAND WITHOUT PRIOR DB DUMP
            raise RuntimeError(
                "Found more pages than Root+Home. Aborting. use force=1 to overwrite"
            )

        self.setup_homepage(page_app, page_model, host_name, site_name)
        if verbosity > 0:
            msg = "New homepage + site successfully created."
            self.stdout.write(msg)

    def setup_homepage(
        self, page_app: str, page_model: str, host_name: str, site_name: str
    ):
        ContentType = apps.get_model("contenttypes.ContentType")
        Site = apps.get_model("wagtailcore.Site")
        CustomPage = apps.get_model(f"{page_app}.{page_model}")

        # Create or read cms page content type
        cms_page_content_type, created = ContentType.objects.get_or_create(  # type: ignore
            model=page_model,
            app_label=page_app,
        )

        # Delete the default home page generated by wagtail,
        # and replace it with a more useful page type.
        # Note: this also deletes the default site
        _ = Page.objects.filter(slug="home").delete()

        try:
            root_page = Page.objects.get(path="0001")
        except Page.DoesNotExist:
            # root page not found, something is seriously wrong
            exit()

        homepage = CustomPage(  # type: ignore
            title="Home",
            slug="home",
            content_type=cms_page_content_type,
            # path="00010001",
            # depth=2,
            # numchild=0,
            # url_path="/home/",
            # locale_id=Locale.get_default().id,
        )
        root_page.add_child(instance=homepage)
        homepage.save_revision().publish()

        # Create a new default site
        Site.objects.create(  # type: ignore
            hostname=host_name,
            site_name=site_name,
            root_page_id=homepage.id,
            is_default_site=True,
        )
