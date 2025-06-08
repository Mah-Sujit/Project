```python
# Title: Text-based RPG Simulation in Django

from django.db import models
from django.http import JsonResponse
from django.views import View
import random

# Character model with basic attributes.
class Character(models.Model):
    name = models.CharField(max_length=100)
    health = models.IntegerField(default=100)
    strength = models.IntegerField(default=10)

    def attack(self, other_character):
        """Simulates an attack on another character, reducing their health."""
        damage = random.randint(1, self.strength)
        other_character.health = max(0, other_character.health - damage)
        other_character.save()
        return damage

# JSON utility function for error handling.
def json_response(data, status=200):
    """Utility function to return a JSON response with error handling."""
    try:
        return JsonResponse(data, status=status)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

# View for handling character interactions.
class CharacterInteractionView(View):

    def post(self, request, *args, **kwargs):
        """Handles POST requests to simulate character attacks."""
        try:
            attacker_id = request.POST.get('attacker_id')
            defender_id = request.POST.get('defender_id')

            attacker = Character.objects.get(id=attacker_id)
            defender = Character.objects.get(id=defender_id)

            damage = attacker.attack(defender)

            response_data = {
                'message': f"{attacker.name} attacked {defender.name} causing {damage} damage.",
                'attacker_health': attacker.health,
                'defender_health': defender.health
            }
            return json_response(response_data)

        except Character.DoesNotExist:
            return json_response({'error': 'Character not found.'}, status=404)
        except Exception as e:
            return json_response({'error': 'An unexpected error occurred: ' + str(e)}, status=500)
```

This code snippet defines a simple text-based RPG simulation using Django. It includes a `Character` model that can attack another character, a view to handle the attack interaction, and utility for JSON responses with error handling.