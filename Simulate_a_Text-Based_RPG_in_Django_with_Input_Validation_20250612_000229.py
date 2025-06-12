Title: Simulate a Text-Based RPG in Django with Input Validation

```python
from django.http import JsonResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
import json
import random

# A simple RPG character class
class Character:
    def __init__(self, name):
        self.name = name
        self.health = 100
        self.attack_power = 10
        self.defense = 5

    def attack(self, target):
        damage_dealt = max(self.attack_power - target.defense, 0)
        target.health -= damage_dealt
        return damage_dealt

    def is_alive(self):
        return self.health > 0

# A dictionary to store active characters
characters = {}

# Utility function to validate character existence
def validate_character(name):
    return name in characters

# View for interacting with the RPG
@method_decorator(csrf_exempt, name='dispatch')
class RPGView(View):

    # Standard Django method for post requests
    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            action = data.get('action')
            if action not in ('create', 'attack', 'status'):
                return JsonResponse({'error': 'Invalid action'}, status=400)

            # Handle character creation
            if action == 'create':
                name = data.get('name')
                if not name or not isinstance(name, str) or name in characters:
                    return JsonResponse({'error': 'Invalid or duplicate name'}, status=400)

                characters[name] = Character(name)
                return JsonResponse({'message': f'Character {name} created'})

            # Handle attacking another character
            elif action == 'attack':
                attacker_name = data.get('attacker')
                target_name = data.get('target')

                if not validate_character(attacker_name) or not validate_character(target_name):
                    return JsonResponse({'error': 'Invalid attacker or target'}, status=400)

                attacker = characters[attacker_name]
                target = characters[target_name]

                if not attacker.is_alive() or not target.is_alive():
                    return JsonResponse({'error': 'Attacker or target is dead'}, status=400)

                damage = attacker.attack(target)
                return JsonResponse({'message': f'{attacker_name} attacked {target_name} for {damage} damage'})

            # Handle checking character status
            elif action == 'status':
                name = data.get('name')
                
                if not validate_character(name):
                    return JsonResponse({'error': 'Invalid character name'}, status=400)
                
                character = characters[name]
                return JsonResponse({'name': character.name, 'health': character.health})

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
```

In this Django view, we simulate a basic text-based RPG where users can create characters, perform attacks, and check character status. We make sure to validate inputs for proper structure and content, ensuring characters exist before interacting with them. The simplicity of this script adheres to the constraint of 50% complexity.