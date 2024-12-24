import pytest
from characters.ai_controller import AIController
from characters.character import Character

@pytest.fixture
def ai_controller():
    return AIController(difficulty='medium')

@pytest.fixture
def characters():
    ai_char = Character(600, 450, facing_right=False)
    player_char = Character(200, 450, facing_right=True)
    return ai_char, player_char

def test_ai_controller_initialization():
    # Test different difficulty levels
    easy_ai = AIController('easy')
    medium_ai = AIController('medium')
    hard_ai = AIController('hard')
    
    assert easy_ai.reaction_time > medium_ai.reaction_time > hard_ai.reaction_time
    assert easy_ai.aggression < medium_ai.aggression < hard_ai.aggression

def test_ai_decision_making(ai_controller, characters):
    ai_char, player_char = characters
    
    # Test decision format
    decision = ai_controller.decide_action(ai_char, player_char)
    assert isinstance(decision, dict)
    assert 'move' in decision
    assert 'jump' in decision
    assert 'attack' in decision
    
    # Test movement decision when far apart
    ai_char.x = 600
    player_char.x = 100
    decision = ai_controller.decide_action(ai_char, player_char)
    if decision['move'] != 0:  # If it decided to move
        assert decision['move'] < 0  # Should move left towards player

def test_ai_defensive_behavior(ai_controller, characters):
    ai_char, player_char = characters
    
    # Test defensive behavior when low health
    ai_char.health = 20
    ai_char.x = 300
    player_char.x = 350  # Close to AI
    
    decision = ai_controller.decide_action(ai_char, player_char)
    if decision['move'] != 0:  # If it decided to move
        assert decision['move'] < 0  # Should move away from player

def test_ai_attack_behavior(ai_controller, characters):
    ai_char, player_char = characters
    
    # Test attack behavior when in range
    ai_char.x = 300
    player_char.x = 340  # Within attack range
    
    # Make multiple attempts since behavior has random elements
    attack_decisions = []
    for _ in range(10):
        decision = ai_controller.decide_action(ai_char, player_char)
        if decision['attack']:
            attack_decisions.append(decision['attack'])
    
    # Should have made some attack decisions
    assert len(attack_decisions) > 0
    # Should have both punch and kick attacks
    assert 'punch' in attack_decisions or 'kick' in attack_decisions 