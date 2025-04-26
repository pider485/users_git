#uvicorn main:app --reload
from fastapi import FastAPI , Query
from pydantic import BaseModel, Field
from typing import Union

app = FastAPI()

all_books = {
    "Джордж Оруелл": [["1984", 328], ["Колгосп тварин", 112]],
    "Стівен Кінг": [["Воно", 1138], ["Сяйво", 447]],
    "Артур Конан Дойл": [["Пригоди Шерлока Холмса", 307], ["Собака Баскервілів", 256]],
    "Джоан Роулінг": [["Гаррі Поттер і філософський камінь", 223], ["Гаррі Поттер і таємна кімната", 251]],
    "Лев Толстой": [["Війна і мир", 1225], ["Анна Кареніна", 864]]
}

@app.get("/")
async def index():
    """
    пр
    """
    return{
        "message: пр"
    }

class Book(BaseModel):
    author: str = Field(..., min_lenght=3, max_lenght=255)
    pages: int = Field(..., g=10)
    gr:int

@app.get("/")
async def get_all_books():
    """
    Повертає список всіх книг
    """
    return all_books

@app.post("/add_book")
async def add_new_book(book:Book):
    if book.author not in all_books:
        all_books[book.author] = [[book.title, book.pages]]
    else:
        all_books[book.author].append(book.title, book.pages)

    return {'message': "Книга створена"}

@app.get('/author/{author}')
async def get_author_books(author:str):
    if author in all_books:
        return all_books[author]
    else:
        return {'message': "Книг автора не знайдено"}

@app.put('/{author}/{book_title}')
async def update_book_pages(author : str , book_title : str, 
                            new_pages : int = Query(gt=10, title="Нова кількість сторінок",
                            description='Нова кількість сторінок у данній книзі')):
    if author in all_books:
        for book in all_books[author]:
            if book[0] == book_title:
                book[1] = new_pages
                return {"message": 'update'}
    return  {'error' : 'not find'}
    
@app.delete('/{author}/{book_title}')
async def delete_book(author : str , book_title : str):
    if author in all_books:
        for book in all_books[author]:
            if book[0] == book_title:
                all_books[author].remove(book)
                return {'message': "Gotovo"}
    return {'error' : 'not find'}