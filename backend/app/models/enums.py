from enum import Enum


class FrequencyType(str, Enum):
    """Frequency types for habits"""

    EVERY_30_MIN = "every_30_min"
    HOURLY = "hourly"
    EVERY_3_HOURS = "every_3_hours"
    EVERY_6_HOURS = "every_6_hours"
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"

    @classmethod
    def choices(cls):
        """Return list of all frequency choices"""
        return [freq.value for freq in cls]

    @classmethod
    def is_valid(cls, value):
        """Check if value is a valid frequency"""
        return value in cls.choices()

    def __str__(self):
        return self.value


class HabitIcon(str, Enum):
    """Available icons for habits"""

    WATER = "water"
    FITNESS = "fitness"
    BOOK = "book"
    BED = "bed"
    RESTAURANT = "restaurant"
    LEAF = "leaf"
    MEDICAL = "medical"
    WALK = "walk"
    BICYCLE = "bicycle"
    PIZZA = "pizza"
    MOON = "moon"
    SUNNY = "sunny"
    HEART = "heart"
    FLAME = "flame"
    MUSICAL_NOTES = "musical-notes"
    BARBELL = "barbell"
    CAFE = "cafe"
    BRUSH = "brush"
    CODE = "code"
    GAME_CONTROLLER = "game-controller"
    CAMERA = "camera"
    FOOTBALL = "football"
    LANGUAGE = "language"
    PENCIL = "pencil"
    SCHOOL = "school"
    TIMER = "timer"
    PHONE_PORTRAIT = "phone-portrait"
    MAIL = "mail"
    CHATBUBBLES = "chatbubbles"
    CAR = "car"
    TRAIN = "train"
    AIRPLANE = "airplane"
    HOME = "home"
    BUSINESS = "business"
    WALLET = "wallet"
    CART = "cart"
    GIFT = "gift"
    FLOWER = "flower"
    SNOW = "snow"
    STAR = "star"
    TROPHY = "trophy"
    RIBBON = "ribbon"
    SPARKLES = "sparkles"
    ROCKET = "rocket"
    BULB = "bulb"
    MEGAPHONE = "megaphone"
    HOURGLASS = "hourglass"
    CALENDAR = "calendar"
    ALARM = "alarm"
    EYE = "eye"
    GLASSES = "glasses"
    HEADSET = "headset"
    MAP = "map"
    LOGO_TIKTOK = "logo-tiktok"
    LOGO_INSTAGRAM = "logo-instagram"

    @classmethod
    def choices(cls):
        """Return list of all icon choices"""
        return [icon.value for icon in cls]

    @classmethod
    def is_valid(cls, value):
        """Check if value is a valid icon"""
        return value in cls.choices()

    def __str__(self):
        return self.value
