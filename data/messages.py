from random import randint

class WadsworthMsg:

    def greetings(self, token=None):
        pass

    def affirmations(self, token=None):
        messages = [
            f'Very good.',
            f'Very good, {token}.',
            f'Very well.',
            f'Very well {token}.',
            'Indeed.',
            'Certainly.',
            f'Certainly {token}.',
        ]
        return str(messages[randint(0, len(messages)-1)])
    
    def error_msgs(self, token=None):
        messages = [
            'I think you may be mistaken.',
            'I am afraid I disagree with your request.',
            f'Pardon me {token}.',
            f'Pardon me.',
            'I most graciously apologize.',
            f'I hope you will forgive me {token}.',
            f'I hope you will forgive me.',
            'I seem to be having troubles.',
        ]
        return str(messages[randint(0, len(messages)-1)])

    def retrieval_messages(self, token=None):
        messages = [
            'Allow me a moment to gather that for you',
            'Please give me a few moments',
            'I shall begin searching now',
            'I hope to bring you what you need',
            'I will look for that right away',
        ]
        return str(messages[randint(0, len(messages)-1)])

    def trash_talk(self, token=None):
        if not token:
            token = ''
        messages = [
            f"I don't have the energy to pretend to like you today, {token}",
            f"What? You like to talk behind my back {token}?",
            f"Sweetie, leave the sarcasm and insults to the pros. You're going to hurt yourself",
            f"Hey! Go play in traffic {token}...",
            f"If I give you a straw, will you go and suck the joy out of someone else's life?",
            f"If you didn't want sarcastic answers, you shouldn't ask stupid questions, {token}",
            f"My silence is not a weakness, it's the beginning of my revenge",
            f"{token}, you are the reason they put instructions on shampoo .",
            ]
        return str(messages[randint(0, len(messages)-1)])

    def debanair_messages(self, token):
        return f'{self.affirmations(token)} {self.retrieval_messages(token)}'