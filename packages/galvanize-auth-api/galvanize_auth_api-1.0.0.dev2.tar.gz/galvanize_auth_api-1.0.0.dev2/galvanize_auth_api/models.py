from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from .info_utils import FromDictMixin


@dataclass
class ProductBranding(FromDictMixin):
    """A DTO that represents a product's branding."""

    id: int
    """The identifier for the specific branding"""

    registration_title: str
    """The title shown on the registration page"""

    registration_paragraph: str
    """The paragraph of text shown on the registration page"""

    logo_url: str
    """The URL of the logo shown on the registration page"""

    nav_logo: str
    """The URL of the logo to show for the product in the nav bar"""

    welcome_title: str
    """The title of the welcome page"""

    welcome_access_message: str
    """The message to show when the registrant access the branded product"""

    welcome_course_button: str
    """The text for the button for the branded product"""

    confirm_account_message: str
    """The message to show to confirm the registrant's account"""

    confirm_product_title: str
    """The title of the product to show on the confirmation page"""

    form_type: str
    """The type of form to show based for the brand"""

    email_label: str
    """The customized label for the email input for the brand"""


@dataclass
class ProductInfo(FromDictMixin):
    """A DTO that represents a Galvanize Learning Platform product."""

    branding: Optional[ProductBranding]
    """What company the product is branded to"""

    campus_name: str
    """The name of the campus where the product is hosted"""

    category: str
    """The category: immersive, prep, assessment, workshop, or other"""

    client: str
    """The name of the organization to which the product is delivered"""

    cohort_code: str
    """The internal code used to reference the cohort"""

    copy_of: Optional[str]
    """The id of the product from which this is copied"""

    created_at: datetime
    """The timestamp for when the product was created"""

    display_name: str
    """The name to display for the product"""

    ends_on: datetime
    """The date on which the product ends"""

    format: str
    """The format of the product: full time, part time, other"""

    id: int
    """The integer identifier for the product"""

    label: str
    """The label for the product"""

    learn_v2: bool
    """A flag to indicate if it is served by Learn v2"""

    name: str
    """The name of the product"""

    opt_out_for_marketing: bool
    """A flag to indicate if registrants opt out of marketing"""

    product_type: str
    """The program that the product belongs to

    Valid values: enterprise, consumer, military, third-party,
        internal, or other
    """

    program: str
    """The number of people registered for the product"""

    registrations_count: int
    """The number of registrants in the product"""

    salesforce_ids: List[str]
    """The Salesforce-specific identifiers for the product"""

    self_registerable: bool
    """A flag to indicate if registrants can register themselves"""

    slug: str
    """The URL-friendly slug for the product"""

    starts_on: datetime
    """The date on which the product starts"""

    subject: str
    """The subject of the content

    Valid values: data science, software engineering, or other
    """

    type: str
    """The type or structure of the product

    Valid values: SEI, DSI, or other
    """

    uid: str
    """The alphanumeric unique identifier for the product"""

    used_by_application: str
    """A list of applications that use the product"""


@dataclass
class UserInfo(FromDictMixin):
    """A DTO that represents a Galvanize Learning Platform user."""

    id: int
    type: str
    uid: str
    first_name: str
    last_name: str
    email: str
    github_username: str
    roles: List[str]
    timezone: str
    terms_accepted_at: datetime
    confirmed_at: datetime
    created_at: datetime
    updated_at: datetime
    phone: str
    profile_image: str
    galvanize_id: str
    sign_in_count: int
    is_opted_out_of_emails: bool
    preferred_campus: str
    relationships: dict
    data: dict


@dataclass
class TokenInfo(FromDictMixin):
    """A DTO that represents token information from the OAuth workflow."""

    resource_owner_id: Optional[str]
    scope: List[str]
    expires_in: timedelta
    application: Dict[str, str]
    created_at: datetime
