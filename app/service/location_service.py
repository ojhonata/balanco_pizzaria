from sqlalchemy.orm import Session

from app.models.location import Location
from app.repository import location_repository
from app.schemas.location_schema import LocationCreate


def get_all(session: Session) -> list[Location]:
    return location_repository.get_all_location(session)


def get_location_by_id(session: Session, id: int) -> list[Location]:
    location = location_repository.get_by_id(session, id)

    if not location:  # se localizacao nao foi encontrada
        raise ValueError("Localização não encontrada")

    return location


def post_location(session: Session, data: LocationCreate) -> Location:
    existing_location = location_repository.get_by_name(session, data.name)

    if existing_location:
        raise ValueError("Localização já cadastrada")
    return location_repository.create_location(session, data)
