class ButtonStyle:
    PRIMARY = 1
    SECONDARY = 2
    SUCCESS = 3
    DANGER = 4
    LINK = 5

class Button:
    def __init__(
        self,
        style: int = ButtonStyle.PRIMARY,
        label: str = '',
        custom_id: str = '',
        url: str = None,
        emoji: dict = None,
        disabled: bool = False
    ):  
        self.base = {
            "type": 2,
            "style": style,
            "label": label,
            "custom_id": custom_id,
            "disabled": disabled
        }

        if emoji is not None:
            self.base['emoji'] = emoji
        
        if style == ButtonStyle.LINK:
            self.base["url"] = url

    def build(self):
        return self.base