from datetime import datetime, timedelta, timezone
from typing import Dict, Optional, Union
import logging

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.db.orm_models import Usuario, UserRole
from app.repositories.usuario_repository import UsuarioRepository
from app.db.session import get_db
from app.models.usuario import UsuarioBase, UsuarioInDB, TokenData

# Configuração de segurança
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/backend/v1/auth/token", auto_error=False)

# Funções de segurança
def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifica se a senha informada corresponde ao hash armazenado."""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """Gera um hash seguro para a senha informada."""
    return pwd_context.hash(password)

def create_access_token(subject: Union[str, int], expires_delta: Optional[timedelta] = None) -> str:
    """
    Cria um token JWT de acesso.
    
    Args:
        subject: Identificador do usuário (username)
        expires_delta: Tempo de expiração do token
        
    Returns:
        Token JWT codificado
    """
    if not settings.SECRET_KEY or len(settings.SECRET_KEY) < 32 or settings.ALGORITHM != 'HS256':
        raise HTTPException(status_code=503, detail='Authentication is not configured.')
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    # Criar payload com 'sub' (subject) e 'exp' (expiration time)
    to_encode = {"sub": str(subject), "exp": expire}
    
    # Codificar o token
    encoded_jwt = jwt.encode(
        to_encode, 
        settings.SECRET_KEY, 
        algorithm=settings.ALGORITHM
    )
    
    return encoded_jwt

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db),
) -> Usuario:
    """Valida o JWT e carrega o usuário real do banco de dados."""
    if not settings.SECRET_KEY or len(settings.SECRET_KEY) < 32 or settings.ALGORITHM != "HS256":
        raise HTTPException(status_code=503, detail="Authentication is not configured.")
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        subject = payload.get("sub")
    except JWTError:
        subject = None
    if not isinstance(subject, str) or not subject.strip():
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication token.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    repository = UsuarioRepository(db)
    user = await repository.get_by_email(subject)
    if not user or not user.ativo:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User unavailable.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


async def get_current_admin_user(
    user: Usuario = Depends(get_current_user),
) -> Usuario:
    """Exige uma conta ativa com perfil administrador."""
    if user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Administrator permissions required.",
        )
    return user


# Função adicional para autenticação com WEG SSO (mock)
async def authenticate_with_weg_sso(token: str) -> Optional[UsuarioBase]:
    """
    Autentica um usuário através do SSO da WEG.
    
    Args:
        token: Token de autenticação SSO
        
    Returns:
        Dados do usuário autenticado ou None se a autenticação falhar
    """
    # Aqui seria implementada a lógica de verificação do token SSO com o sistema da WEG
    # Esta é uma implementação mock para demonstração
    
    # Em um cenário real, chamaríamos a API de autenticação da WEG
    # e receberíamos os dados do usuário
    
    return None  # Mock - implementação real seria feita conforme especificações da WEG