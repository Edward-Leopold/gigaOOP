from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from db.models.quiz import Quiz, QuizQuestion, QuizQuestionAnswer
from db.schemas.quiz import QuizCreate, QuizRead, QuizUpdate
from api.deps import get_db

router = APIRouter()


@router.post("/", response_model=QuizRead, status_code=status.HTTP_201_CREATED)
async def create_quiz(quiz: QuizCreate, db: AsyncSession = Depends(get_db)):
    new_quiz = Quiz(**quiz.dict(exclude={"questions"}))
    async with db as session:
        session.add(new_quiz)
        await session.commit()
        await session.refresh(new_quiz)

        for question in quiz.questions:
            new_question = QuizQuestion(
                **question.dict(exclude={"answers"}), quiz_id=new_quiz.id
            )
            session.add(new_question)
            await session.commit()
            await session.refresh(new_question)

            for answer in question.answers:
                new_answer = QuizQuestionAnswer(
                    **answer.dict(), question_id=new_question.id
                )
                session.add(new_answer)

        await session.commit()
        await session.refresh(new_quiz)

    return new_quiz


@router.get("/{quiz_id}", response_model=QuizRead)
async def read_quiz(quiz_id: int, db: AsyncSession = Depends(get_db)):
    async with db as session:
        result = await session.execute(select(Quiz).where(Quiz.id == quiz_id))
        quiz = result.scalars().first()
        if not quiz:
            raise HTTPException(status_code=404, detail="Quiz not found")

        result_questions = await session.execute(
            select(QuizQuestion).where(QuizQuestion.quiz_id == quiz.id)
        )
        questions = result_questions.scalars().all()

        for question in questions:
            result_answers = await session.execute(
                select(QuizQuestionAnswer).where(
                    QuizQuestionAnswer.question_id == question.id
                )
            )
            question.answers = result_answers.scalars().all()

        quiz.questions = questions
    return quiz


@router.get("/", response_model=list[QuizRead])
async def get_quizzes(
    skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db)
):
    async with db as session:
        result = await session.execute(select(Quiz).offset(skip).limit(limit))
        quizzes = result.scalars().all()

        for quiz in quizzes:
            result_questions = await session.execute(
                select(QuizQuestion).where(QuizQuestion.quiz_id == quiz.id)
            )
            questions = result_questions.scalars().all()

            for question in questions:
                result_answers = await session.execute(
                    select(QuizQuestionAnswer).where(
                        QuizQuestionAnswer.question_id == question.id
                    )
                )
                question.answers = result_answers.scalars().all()

            quiz.questions = questions
    return quizzes


@router.put("/{quiz_id}", response_model=QuizRead)
async def update_quiz(
    quiz_id: int, quiz_update: QuizUpdate, db: AsyncSession = Depends(get_db)
):
    async with db as session:
        result = await session.execute(select(Quiz).where(Quiz.id == quiz_id))
        quiz = result.scalars().first()
        if not quiz:
            raise HTTPException(status_code=404, detail="Quiz not found")

        update_data = quiz_update.dict(exclude_unset=True)
        for key, value in update_data.items():
            if key == "questions":
                # Handle updating questions and their answers
                await session.execute(
                    select(QuizQuestion).where(QuizQuestion.quiz_id == quiz.id).delete()
                )
                await session.commit()

                for question_data in value:
                    new_question = QuizQuestion(**question_data, quiz_id=quiz.id)
                    session.add(new_question)
                    await session.commit()
                    await session.refresh(new_question)

                    for answer_data in question_data["answers"]:
                        new_answer = QuizQuestionAnswer(
                            **answer_data, question_id=new_question.id
                        )
                        session.add(new_answer)
            else:
                setattr(quiz, key, value)

        session.add(quiz)
        await session.commit()
        await session.refresh(quiz)
    return quiz


@router.delete("/{quiz_id}", response_model=None)
async def delete_quiz(quiz_id: int, db: AsyncSession = Depends(get_db)):
    async with db as session:
        result = await session.execute(select(Quiz).where(Quiz.id == quiz_id))
        quiz = result.scalars().first()
        if not quiz:
            raise HTTPException(status_code=404, detail="Quiz not found")

        await session.execute(
            select(QuizQuestion).where(QuizQuestion.quiz_id == quiz.id).delete()
        )
        await session.commit()

        await session.execute(
            select(QuizQuestionAnswer)
            .where(
                QuizQuestionAnswer.question_id.in_(
                    select(QuizQuestion.id).where(QuizQuestion.quiz_id == quiz.id)
                )
            )
            .delete()
        )
        await session.commit()

        await session.delete(quiz)
        await session.commit()
    return None
