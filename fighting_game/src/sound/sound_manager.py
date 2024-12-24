import pygame
import os

class SoundManager:
    def __init__(self):
        pygame.mixer.init()
        self.current_music = None
        
    def play_stage_music(self, stage_id):
        """Play the appropriate music for the current stage"""
        # Stop any currently playing music
        pygame.mixer.music.stop()
        
        # Determine music file path based on stage
        if isinstance(stage_id, str):
            if stage_id == 'bren':
                music_file = 'stage_1.mid'
            elif stage_id == 'billy':
                music_file = 'stage_2.mid'
            elif stage_id == 'niall':
                music_file = 'stage_3.mid'
            elif stage_id == 'ciaran':
                music_file = 'stage_4.mid'
            elif stage_id == 99:  # Final battle
                music_file = 'stage_5.mid'
            else:
                music_file = 'stage_1.mid'  # Default to stage 1 music
        else:
            music_file = 'stage_1.mid'  # Default to stage 1 music
            
        # Try to load and play the music file
        try:
            # Try with fighting_game prefix first
            music_path = os.path.join("fighting_game", "assets", "sounds", music_file)
            if not os.path.exists(music_path):
                # Try without prefix
                music_path = os.path.join("assets", "sounds", music_file)
                
            if os.path.exists(music_path):
                print(f"Loading stage music from: {music_path}")
                pygame.mixer.music.load(music_path)
                pygame.mixer.music.play(-1)  # Loop indefinitely
                self.current_music = music_path
            else:
                print(f"Music file not found: {music_path}")
        except Exception as e:
            print(f"Error loading music: {e}")
            
    def stop_music(self):
        """Stop the currently playing music"""
        pygame.mixer.music.stop()
        self.current_music = None 