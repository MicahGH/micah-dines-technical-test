from api.errors import TabClosedError, TabNotFoundError
from api.models import Tab


class TabService:
    """Service class for handling tab-related operations."""

    @staticmethod
    def get_open_tab_or_raise(tab_id: int) -> Tab:
        """Fetch a tab by ID and ensure it is currently OPEN. If not, raise an error."""
        try:
            tab = Tab.objects.get(pk=tab_id)
        except Tab.DoesNotExist as err:
            msg = f"Tab with id {tab_id} does not exist."
            raise TabNotFoundError(msg) from err

        if tab.status != Tab.Status.OPEN.value:
            msg = f"Tab with id {tab_id} is already closed."
            raise TabClosedError(msg)

        return tab
