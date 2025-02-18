from django.db import migrations
from django.utils.text import slugify

def populate_slugs(apps, schema_editor):
    Category = apps.get_model('myapp', 'Category')
    for category in Category.objects.all():
        base_slug = slugify(category.name)
        slug = base_slug
        counter = 1
        
        # Check for existing slugs to ensure uniqueness
        while Category.objects.filter(slug=slug).exists():
            slug = f"{base_slug}-{counter}"
            counter += 1
            
        category.slug = slug
        category.save()

class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0004_add_category_slug'),  # Make sure this matches your previous migration
    ]

    operations = [
        migrations.RunPython(populate_slugs),
    ]