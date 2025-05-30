from django.apps import AppConfig, apps
from django.db.models.signals import post_migrate

class CoreConfig(AppConfig):
    name = "core"

    def ready(self):
        from django.contrib.auth.models import Group, Permission
        from django.contrib.contenttypes.models import ContentType

        def create_roles(sender, **kwargs):
            # Ensure the two main groups exist
            admin_group, _ = Group.objects.get_or_create(name="Admin")
            user_group, _  = Group.objects.get_or_create(name="User")

            try:
                # Assign permissions for the Movie model
                from movies.models import Movie
                ct    = ContentType.objects.get_for_model(Movie)
                perms = Permission.objects.filter(content_type=ct)

                # Admin: full CRUD
                admin_group.permissions.set(perms)

                # User: only view
                view_perm = Permission.objects.get(
                    codename="view_movie",
                    content_type=ct
                )
                user_group.permissions.set([view_perm])

                print("✅ RBAC permissions loaded successfully.")
            except Exception as e:
                print(f"⚠ Error loading RBAC permissions: {e}")

        # Sadece 'movies' app’inin migrasyonu tamamlandığında çalışsın
        post_migrate.connect(
            create_roles,
            sender=apps.get_app_config("movies")
        )
