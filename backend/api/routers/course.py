from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select


from db.models.course import Course
from db.schemas.course import CourseCreate, CourseUpdate, CourseRead
from api.deps import get_db


router = APIRouter()


@router.post("/", response_model=CourseRead)
async def create_course(course: CourseCreate, db: AsyncSession = Depends(get_db)):
    db_course = Course(**course.dict())
    db.add(db_course)
    await db.commit()
    await db.refresh(db_course)
    return db_course


@router.get("/{course_id}", response_model=CourseRead)
async def read_course(course_id: int, db: AsyncSession = Depends(get_db)):
    course = await db.get(Course, course_id)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    return course


@router.get("/", response_model=list[CourseRead])
async def get_courses(
    skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db)
):
    async with db as session:
        result = await session.execute(select(Course).offset(skip).limit(limit))
        courses = result.scalars().all()
    return courses


@router.put("/{course_id}", response_model=CourseRead)
async def update_course(
    course_id: int, course: CourseUpdate, db: AsyncSession = Depends(get_db)
):
    async with db as session:
        result = await session.execute(select(Course).where(Course.id == course_id))
        db_course = result.scalars().first()
        if db_course is None:
            raise HTTPException(status_code=404, detail="Course not found")

        for var, value in vars(course).items():
            setattr(db_course, var, value) if value else None

        session.add(db_course)
        await session.commit()
        await session.refresh(db_course)
    return db_course


@router.delete("/{course_id}", response_model=None)
async def delete_course(course_id: int, db: AsyncSession = Depends(get_db)):
    async with db as session:
        result = await session.execute(select(Course).where(Course.id == course_id))
        db_course = result.scalars().first()
        if db_course is None:
            raise HTTPException(status_code=404, detail="Course not found")

        await session.delete(db_course)
        await session.commit()
    return None
