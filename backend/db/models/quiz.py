from sqlalchemy import Column, Integer, String, ForeignKey, Boolean

from db.session import Base


class Quiz(Base):
    __tablename__ = "quizzes"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    theme_id = Column(Integer, ForeignKey("themes.id"), nullable=False)


class QuizQuestion(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True)
    question_text = Column(String, index=True)
    quiz_id = Column(Integer, ForeignKey("quizzes.id"), nullable=False)


class QuizQuestionAnswer(Base):
    __tablename__ = "answers"

    id = Column(Integer, primary_key=True, index=True)
    answer_text = Column(String, index=True)
    is_correct = Column(Boolean, default=False)
    question_id = Column(Integer, ForeignKey("questions.id"), nullable=False)
