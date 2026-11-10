import logging
import os
from sqlalchemy.orm import Session
from app.core.config import settings
from app.core.security import get_password_hash
from app.db import base  # noqa: F401
from app.db.orm_models import Usuario, UserRole, StatusProjeto, Configuracao

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Função para criar usuário administrador inicial
def create_first_admin(db: Session) -> None:
    """Cria o administrador somente quando configurado explicitamente."""
    if db.query(Usuario).first():
        return
    email = os.getenv("INITIAL_ADMIN_EMAIL", "").strip()
    password = os.getenv("INITIAL_ADMIN_PASSWORD", "")
    if not email or not password:
        logger.info("Administrador inicial não configurado; cadastro ignorado.")
        return
    if len(password) < 12:
        raise ValueError("A senha inicial deve conter pelo menos 12 caracteres.")
    admin = Usuario(
        nome=os.getenv("INITIAL_ADMIN_NAME", "Administrador"),
        email=email,
        senha_hash=get_password_hash(password),
        role=UserRole.ADMIN,
        ativo=True,
    )
    db.add(admin)
    db.commit()
    logger.info("Administrador inicial criado.")


# Função para criar status de projetos padrão
def create_default_status(db: Session) -> None:
    # Verificar se já existem status
    status_count = db.query(StatusProjeto).count()
    if status_count == 0:
        status_list = [
            StatusProjeto(nome="Não Iniciado", descricao="Projeto ainda não iniciado", is_final=False, ordem_exibicao=1),
            StatusProjeto(nome="Em Andamento", descricao="Projeto em execução", is_final=False, ordem_exibicao=2),
            StatusProjeto(nome="Pausado", descricao="Projeto temporariamente pausado", is_final=False, ordem_exibicao=3),
            StatusProjeto(nome="Concluído", descricao="Projeto finalizado com sucesso", is_final=True, ordem_exibicao=4),
            StatusProjeto(nome="Cancelado", descricao="Projeto cancelado", is_final=True, ordem_exibicao=5)
        ]
        db.add_all(status_list)
        db.commit()
        logger.info("Status de projetos padrão criados com sucesso!")
    else:
        logger.info("Status de projetos já existem no banco de dados.")

# Função para criar configurações iniciais
def create_default_configs(db: Session) -> None:
    # Verificar se já existem configurações
    config_count = db.query(Configuracao).count()
    if config_count == 0:
        configs = [
            Configuracao(chave="jira_sync_enabled", valor="false", descricao="Define se a sincronização com o Jira está habilitada"),
            Configuracao(chave="jira_sync_interval", valor="60", descricao="Intervalo de sincronização com o Jira em minutos"),
            Configuracao(chave="hora_padrao_dia", valor="8", descricao="Quantidade padrão de horas disponíveis por dia útil"),
        ]
        db.add_all(configs)
        db.commit()
        logger.info("Configurações padrão criadas com sucesso!")
    else:
        logger.info("Configurações já existem no banco de dados.")

# Função para inicializar o banco com dados básicos
def init_db(db: Session) -> None:
    try:
        create_first_admin(db)
        create_default_status(db)
        create_default_configs(db)
        logger.info("Banco de dados inicializado com sucesso!")
    except Exception as e:
        logger.error(f"Erro ao inicializar o banco de dados: {str(e)}")

if __name__ == "__main__":
    from app.db.session import SessionLocal
    
    db = SessionLocal()
    try:
        init_db(db)
    finally:
        db.close() 