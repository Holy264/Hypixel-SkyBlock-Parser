from sqlalchemy.ext.asyncio import AsyncSession

class Baserepository:
    def __init__(self, session: AsyncSession):
        self.session = session
        
