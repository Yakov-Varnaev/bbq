import pytest

from companies.models import MasterProcedure

pytestmark = [pytest.mark.django_db]


def test_master_procedure_is_archived_after_deletion(master_procedure: MasterProcedure):
    master_procedure.delete()
    master_procedure.refresh_from_db()

    assert MasterProcedure.include_archived.get(id=master_procedure.id, archived__isnull=False)


def test_master_procedure_can_be_restored(archived_master_procedure: MasterProcedure):
    archived_master_procedure.restore()
    archived_master_procedure.refresh_from_db()

    assert MasterProcedure.objects.get(id=archived_master_procedure.id).archived is None
