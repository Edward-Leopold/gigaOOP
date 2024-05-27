from sqlalchemy import Column, String, ForeignKey, Integer, Text

from db.session import Base


class Theme(Base):
    __tablename__ = "themes"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    content = Column(Text, index=True)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)
