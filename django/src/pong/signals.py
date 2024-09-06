from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.contrib.auth import get_user_model
import uuid


User = get_user_model()

@receiver(post_migrate)
def create_AI_player(sender, **kwargs):
	ai_user, created = User.objects.get_or_create(
		username='aiskosong',
		defaults={
			'email': 'ai@aispong.ai',
			'first_name': 'AI',
			'last_name': 'Kosong',
			'is_active': True,
			'is_staff': False,
			'is_superuser': False,
		}
	)
	
	if created:
		ai_user.set_password(str(uuid.uuid4()))
		ai_user.save()

		profile = ai_user.profile
		profile.nickname = 'AIs Kosong'
		profile.bio = "I am unbeatable!"
		profile.avatar = 'aibot.jpg'
		profile.save()
	
	
	