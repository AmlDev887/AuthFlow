from pydantic import BaseModel, EmailStr, ConfigDict, Field, field_validator
import re

class AuthLogin(BaseModel):

    username: str = Field(..., min_length=4, max_length= 15)
    login: EmailStr
    parol: str = Field(..., min_length=8, max_length=20)
    
    model_config = ConfigDict(from_attributes=True)

class AuthVerify(BaseModel):

    email: EmailStr 
    code: str = Field(..., min_length=6, max_length=100)

    @field_validator("code")
    @classmethod
    def scanner(cls, value):
        """проверка кода """
        number = value.strip().replace(" ", "")

        if not re.fullmatch(r"\d{6}", number):
            raise ValueError("Код подтверждения должен состоять ровно из 6 цифр")

        return number