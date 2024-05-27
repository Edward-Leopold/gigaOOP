from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select


from db.models.theme import Theme
from db.schemas.theme import ThemeCreate, ThemeUpdate, ThemeRead
from api.deps import get_db

router = APIRouter()


@router.post("/", response_model=ThemeRead, status_code=status.HTTP_201_CREATED)
async def create_theme(theme: ThemeCreate, db: AsyncSession = Depends(get_db)):
    db_theme = Theme(**theme.dict())
    db.add(db_theme)
    await db.commit()
    await db.refresh(db_theme)
    return db_theme


@router.get("/{theme_id}", response_model=ThemeRead)
async def read_theme(theme_id: int, db: AsyncSession = Depends(get_db)):
    theme = await db.get(Theme, theme_id)
    if not theme:
        raise HTTPException(status_code=404, detail="Theme not found")
    return theme


@router.get("/", response_model=list[ThemeRead])
async def get_themes(
    skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db)
):
    async with db as session:
        result = await session.execute(select(Theme).offset(skip).limit(limit))
        themes = result.scalars().all()
    return themes


@router.put("/{theme_id}", response_model=ThemeRead)
async def update_theme(
    theme_id: int, theme: ThemeUpdate, db: AsyncSession = Depends(get_db)
):
    async with db as session:
        result = await session.execute(select(Theme).where(Theme.id == theme_id))
        db_theme = result.scalars().first()
        if db_theme is None:
            raise HTTPException(status_code=404, detail="Theme not found")

        update_data = theme.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_theme, key, value)

        session.add(db_theme)
        await session.commit()
        await session.refresh(db_theme)
    return db_theme


@router.delete("/{theme_id}", response_model=None)
async def delete_theme(theme_id: int, db: AsyncSession = Depends(get_db)):
    async with db as session:
        result = await session.execute(select(Theme).where(Theme.id == theme_id))
        db_theme = result.scalars().first()
        if db_theme is None:
            raise HTTPException(status_code=404, detail="Theme not found")

        await session.delete(db_theme)
        await session.commit()
    return None
