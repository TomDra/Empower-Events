import json
from django.core.management.base import BaseCommand
from myapi.models import User, Charity, ActivityLeader, Activity, AgeGroup

class Command(BaseCommand):
	help = 'Seeds the database with sample data'

	def handle(self, *args, **kwargs):
		# Load data from JSON file
		with open('sample.json', 'r') as file:
			data = json.load(file)

		# Seed Users
		for user_data in data['users']:
			username = user_data['username']
			# Check if user with this username already exists
			if not User.objects.filter(username=username).exists():
				user = User.objects.create_user(
					username=username,
					password=user_data['password'],
					email=user_data['email']
				)
				if 'disabilities' in user_data:
					user.set_disabilities(user_data['disabilities'])
				user.save()
			else:
				print(f"User with username '{username}' already exists. Skipping creation.")

		# Seed Charities
		# Seed Charities
		# Seed Charities
		# Seed Charities
		# Seed Charities
		charity_objs = {}
		for charity_data in data['charities']:
			# Find or create the user associated with the charity
			user, created = User.objects.get_or_create(
				username=charity_data['charity_name'].lower(),
				defaults={'email': charity_data['email']}
			)

			# If the user was just created, print a message
			if created:
				print(f"User '{user.username}' created.")

			# Check if a Charity with the same user already exists
			charity, charity_created = Charity.objects.get_or_create(
				user=user,
				charity_name=charity_data['charity_name'],
				email=charity_data['email']
			)

			# If the charity was just created, print a message
			if charity_created:
				print(f"Charity '{charity.charity_name}' created.")

			# Store the charity object in the dictionary
			charity_objs[charity_data['charity_name']] = charity

		# Seed Activity Leaders
		for leader_data in data['activity_leaders']:
			user = User.objects.get(username=leader_data['user'])
			charity = charity_objs[leader_data['charity']]
			
			# Check if an ActivityLeader with the same user already exists
			if not ActivityLeader.objects.filter(user=user).exists():
				ActivityLeader.objects.create(
					user=user,
					name=leader_data['name'],
					birth_date=leader_data['birth_date'],
					charity=charity,
					email=leader_data['email']
				)
			else:
				print(f"Activity Leader for user '{user.username}' already exists. Skipping creation.")

		# Seed Age Groups
		for age_group_data in data['age_groups']:
			age_group, created = AgeGroup.objects.get_or_create(
				age_range_lower=age_group_data['age_range_lower'],
				age_range_higher=age_group_data['age_range_higher'],
				group_title=age_group_data['group_title']
			)

			# If the age group was just created, print a message
			if created:
				print(f"Age Group '{age_group.group_title}' created.")

		# Seed Activities
		for activity_data in data['activities']:
			# Get the corresponding age group object
			age_group = AgeGroup.objects.get(group_title=activity_data['age_group'])

			# Get the corresponding charity object
			charity = Charity.objects.get(charity_name=activity_data['charity'])

			# Create the activity
			activity, created = Activity.objects.get_or_create(
				description=activity_data['description'],
				latitude=activity_data['latitude'],
				longitude=activity_data['longitude'],
				age_group=age_group,
				charity=charity
			)

			# If the activity was just created, print a message
			if created:
				print(f"Activity '{activity.description}' created.")


		self.stdout.write(self.style.SUCCESS('Database seeded successfully'))
