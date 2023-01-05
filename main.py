import databases

from fastapi import FastAPI
from config import DATABASE_URL, database

from routes import router
    

def create_application(database: databases.Database = None):
    application = FastAPI(title="Boletos 1.0", description="Sistema para gestão de boletos")

    # # register routers
    application.include_router(router, prefix="")

    # # register exception handlers
    # application.add_exception_handler(ExampleException, example_exception_handler)
  
    # set app state
    application.state.database = database

    # base route
    @application.get("/")
    def get_root():
        return {"detail": "Main application"}       

    return application


app = create_application(database=database)

@app.on_event("startup")
async def startup():
    # initialize database
    database_ = app.state.database
    if not database_.is_connected:
        await database_.connect()


@app.on_event("shutdown")
async def shutdown():
    # disconnect from database
    database_ = app.state.database
    if database_.is_connected:
        await database_.disconnect()    
  