"""Module containing element locators for web scraping."""

class ElementLocations:
    """Contains CSS selectors and XPaths for web elements."""
    
    # Search results
    SUBTITLE_ROW = "tr.change"
    EPISODE_ITEM = "div.episode-item"
    TITLE_CELL = "td.name"
    DOWNLOAD_BUTTON = "a.download-subtitle"
    
    # Navigation
    NEXT_PAGE = "a.pagination-next"
    
    # Authentication
    LOGIN_BUTTON = "button[type='submit']"
    USERNAME_FIELD = "input[name='username']"
    PASSWORD_FIELD = "input[name='password']"
    
    # Consent and popups
    COOKIE_CONSENT = "button.cookie-consent-accept"
    CLOSE_POPUP = "button.close-modal" 