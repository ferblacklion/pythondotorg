from django.core.management.base import BaseCommand
from django.conf import settings

from ...models import BlogEntry, RelatedBlog
from ...parser import get_all_entries, update_blog_supernav


class Command(BaseCommand):
    """ Update blog entries and related blog feed data """

    def handle(self, *args, **kwargs):
        # Update PSF Blog
        psf_entries = get_all_entries(settings.PYTHON_BLOG_FEED_URL)

        for entry in psf_entries:
            try:
                e = BlogEntry.objects.get(url=entry['url'])

                # Update our info if it's changed
                if e.pub_date < entry['pub_date']:
                    e.title = entry['title']
                    e.summary = entry['summary']
                    e.pub_date = entry['pub_date']
                    e.save()

            except BlogEntry.DoesNotExist:
                BlogEntry.objects.create(
                    title=entry['title'],
                    summary=entry['summary'],
                    pub_date=entry['pub_date'],
                    url=entry['url'],
                )

        # Update the supernav box with the latest entry's info
        update_blog_supernav()

        # Update Related Blogs
        for blog in RelatedBlog.objects.all():
            blog.update_blog_data()


