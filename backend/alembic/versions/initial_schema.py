"""Initial schema

Revision ID: initial_schema
Revises: 
Create Date: 2024-01-09

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.schema import CreateTable
from sqlalchemy.ext.compiler import compiles

revision = 'initial_schema'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    # Create node_types table first as it has no dependencies
    op.create_table(
        'node_types',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('category', sa.String(), nullable=False),
        sa.Column('description', sa.String(), nullable=True),
        sa.Column('version', sa.String(), nullable=False),
        sa.Column('input_ports', sa.JSON(), nullable=False),
        sa.Column('output_ports', sa.JSON(), nullable=False),
        sa.Column('config_schema', sa.JSON(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )

    # Create workflows table
    op.create_table(
        'workflows',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('description', sa.String(), nullable=True),
        sa.Column('current_version_id', sa.String(), nullable=True),
        sa.Column('global_config', sa.JSON(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )

    # Create workflow_versions table
    op.create_table(
        'workflow_versions',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('workflow_id', sa.String(), nullable=False),
        sa.Column('version', sa.String(), nullable=False),
        sa.Column('description', sa.String(), nullable=True),
        sa.Column('data', sa.JSON(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )

    # Create nodes table
    op.create_table(
        'nodes',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('workflow_id', sa.String(), nullable=False),
        sa.Column('type', sa.String(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('config', sa.JSON(), nullable=True),
        sa.Column('position_x', sa.Float(), nullable=True),
        sa.Column('position_y', sa.Float(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )

    # Create connections table
    op.create_table(
        'connections',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('workflow_id', sa.String(), nullable=False),
        sa.Column('name', sa.String(), nullable=True),
        sa.Column('source_node', sa.String(), nullable=False),
        sa.Column('source_port', sa.String(), nullable=False),
        sa.Column('target_node', sa.String(), nullable=False),
        sa.Column('target_port', sa.String(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )

    # Create workflow_runs table
    op.create_table(
        'workflow_runs',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('workflow_id', sa.String(), nullable=False),
        sa.Column('version_id', sa.String(), nullable=False),
        sa.Column('status', sa.String(), nullable=False),
        sa.Column('start_time', sa.DateTime(), nullable=False),
        sa.Column('end_time', sa.DateTime(), nullable=True),
        sa.Column('logs', sa.JSON(), nullable=True),
        sa.Column('results', sa.JSON(), nullable=True),
        sa.Column('error', sa.String(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )

    # Add foreign key constraints after all tables are created
    op.create_foreign_key('fk_workflow_current_version', 'workflows', 'workflow_versions',
                         ['current_version_id'], ['id'])
    op.create_foreign_key('fk_workflow_version_workflow', 'workflow_versions', 'workflows',
                         ['workflow_id'], ['id'])
    op.create_foreign_key('fk_node_workflow', 'nodes', 'workflows',
                         ['workflow_id'], ['id'])
    op.create_foreign_key('fk_node_type', 'nodes', 'node_types',
                         ['type'], ['id'])
    op.create_foreign_key('fk_connection_workflow', 'connections', 'workflows',
                         ['workflow_id'], ['id'])
    op.create_foreign_key('fk_connection_source', 'connections', 'nodes',
                         ['source_node'], ['id'])
    op.create_foreign_key('fk_connection_target', 'connections', 'nodes',
                         ['target_node'], ['id'])
    op.create_foreign_key('fk_workflow_run_workflow', 'workflow_runs', 'workflows',
                         ['workflow_id'], ['id'])
    op.create_foreign_key('fk_workflow_run_version', 'workflow_runs', 'workflow_versions',
                         ['version_id'], ['id'])

def downgrade():
    # Remove foreign key constraints first
    op.drop_constraint('fk_workflow_run_version', 'workflow_runs', type_='foreignkey')
    op.drop_constraint('fk_workflow_run_workflow', 'workflow_runs', type_='foreignkey')
    op.drop_constraint('fk_connection_target', 'connections', type_='foreignkey')
    op.drop_constraint('fk_connection_source', 'connections', type_='foreignkey')
    op.drop_constraint('fk_connection_workflow', 'connections', type_='foreignkey')
    op.drop_constraint('fk_node_type', 'nodes', type_='foreignkey')
    op.drop_constraint('fk_node_workflow', 'nodes', type_='foreignkey')
    op.drop_constraint('fk_workflow_version_workflow', 'workflow_versions', type_='foreignkey')
    op.drop_constraint('fk_workflow_current_version', 'workflows', type_='foreignkey')

    # Drop tables in reverse order
    op.drop_table('workflow_runs')
    op.drop_table('connections')
    op.drop_table('nodes')
    op.drop_table('workflow_versions')
    op.drop_table('workflows')
    op.drop_table('node_types')
