from app import app, db, bcrypt
from models import User, JournalEntry
from datetime import datetime

def seed_database():
    with app.app_context():
        print("Clearing database...")
        db.drop_all()
        db.create_all()
        
        print("Creating users...")
        users_data = [
            {'username': 'alice', 'password': 'password123'},
            {'username': 'bob', 'password': 'password456'},
            {'username': 'charlie', 'password': 'password789'}
        ]
        
        created_users = []
        for user_data in users_data:
            hashed_password = bcrypt.generate_password_hash(user_data['password']).decode('utf-8')
            user = User(username=user_data['username'], password_hash=hashed_password)
            db.session.add(user)
            created_users.append(user)
        
        db.session.commit()
        print(f"Created {len(created_users)} users")
        
        print("Creating journal entries...")
        journal_entries = [
            {
                'title': 'My First Day',
                'content': 'Today was an amazing day! I started my new journal and I\'m excited to document my journey.',
                'user_index': 0
            },
            {
                'title': 'Learning Flask',
                'content': 'I spent the whole day learning Flask. It\'s such a powerful framework for building web applications.',
                'user_index': 0
            },
            {
                'title': 'Morning Workout',
                'content': 'Woke up early and went for a 5km run. Feeling energized and ready to tackle the day!',
                'user_index': 1
            },
            {
                'title': 'Book Review',
                'content': 'Just finished reading "Clean Code". It has completely changed how I think about writing software.',
                'user_index': 1
            },
            {
                'title': 'Weekend Plans',
                'content': 'Planning to go hiking this weekend. The weather forecast looks perfect!',
                'user_index': 2
            },
            {
                'title': 'Cooking Adventure',
                'content': 'Tried a new recipe today - homemade pasta! It was challenging but so rewarding.',
                'user_index': 2
            },
            {
                'title': 'Project Milestone',
                'content': 'Reached an important milestone in my project. All the hard work is paying off.',
                'user_index': 0
            },
            {
                'title': 'Reflection Time',
                'content': 'Taking some time to reflect on my goals and progress. Sometimes it\'s important to slow down.',
                'user_index': 2
            }
        ]
        
        for entry_data in journal_entries:
            user = created_users[entry_data['user_index']]
            entry = JournalEntry(
                title=entry_data['title'],
                content=entry_data['content'],
                user_id=user.id
            )
            db.session.add(entry)
        
        db.session.commit()
        print(f"Created {len(journal_entries)} journal entries")
        
        print("\nDatabase seeded successfully!")
        print("\nCreated users:")
        for user in created_users:
            print(f"  - {user.username}")
        
        print("\nSample login credentials:")
        print("  Username: alice, Password: password123")
        print("  Username: bob, Password: password456")
        print("  Username: charlie, Password: password789")

if __name__ == '__main__':
    seed_database()
