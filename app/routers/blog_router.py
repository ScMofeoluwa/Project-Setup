from fastapi import APIRouter, Depends, status, HTTPException
from repository import database
from interface import blog_interface
from entity import blog_entity
from sqlalchemy.orm import Session
from blog.repository import blog


router = APIRouter(prefix="/blog", tags=["Blogs"])

get_db = database.get_db


@router.post("/", status_code=status.HTTP_201_CREATED)
def create(request: blog_interface.Blog, db: Session = Depends(get_db)):
    new_blog = blog_entity.Blog(title=request.title, body=request.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


@router.get("/")
def all(db: Session = Depends(get_db)):
    blogs = db.query(blog_entity.Blog).all()
    return blogs


@router.get("/{id}", status_code=status.HTTP_200_OK)
def show(id, response: Response, db: Session = Depends(get_db)):
    blog = db.query(blog_entity.Blog).filter(blog_entity.Blog.id == id).first()
    if not blog:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Blog with the id {id} is not available",
        )
    return blog


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete(id, db: Session = Depends(get_db)):
    blog = db.query(blog_entity.Blog).filter(blog_entity.Blog.id == id)
    if not blog.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Blog with the id {id} is not available",
        )
    blog.delete(synchronize_session=False)
    db.commit()
    return "Blog deleted successfully"


@router.put("/{id}", status_code=status.HTTP_202_ACCEPTED)
def update(id, request: blog_interface.Blog, db: Session = Depends(get_db)):
    blog = db.query(blog_entity.Blog).filter(blog_entity.Blog.id == id)
    if not blog.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Blog with the id {id} is not available",
        )
    blog.update(request.dict(), synchronize_session=False)
    db.commit()
    return "Blog updated successfully"
