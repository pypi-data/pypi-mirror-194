from iotreports_client import Configuration, ApiClient
from iotreports_client.apis import (
    OrganizationApi,
    ReportApi,
    CategoryApi,
    ReportTypeApi,
)
from iotreports_client.models import Report, ReportStreamPayload
import urllib3

urllib3.disable_warnings()

__all__ = [
    "ReportingApi",
    "find_item_id_by_name",
    "find_item_by_name",
    "create_or_update_report",
    "update_report_stream",
]


class ReportingApi:
    def __init__(self, access_token):
        configuration = Configuration(discard_unknown_keys=True)
        configuration.access_token = access_token
        configuration.verify_ssl = False
        self.configuration = configuration
        self.api_client = ApiClient(configuration=configuration)

    @property
    def organzation_api(self):
        return OrganizationApi(self.api_client)

    @property
    def category_api(self):
        return CategoryApi(self.api_client)

    @property
    def report_api(self):
        return ReportApi(self.api_client)

    @property
    def report_type_api(self):
        return ReportTypeApi(self.api_client)


def find_item_id_by_name(name: str, items: list) -> str:
    for item in items:
        if item.name == name:
            return item.id


def find_item_by_name(name: str, items: list) -> object:
    for item in items:
        if item.name == name:
            return item


def create_or_update_report(
        api_key,
        organization_name,
        category_name,
        report_type_name,
        report_name,
        icon,
        report_data,
) -> str:
    reporting_api = ReportingApi(api_key)
    org_id = find_item_id_by_name(
        organization_name, reporting_api.organzation_api.get_organizations()
    )
    report_id = find_item_id_by_name(
        report_name,
        reporting_api.report_api.get_reports(organization_id=org_id).reports,
    )
    if report_id is None:
        category_id = find_item_id_by_name(
            category_name, reporting_api.category_api.get_categories(org_id).categories
        )
        report_type_id = find_item_id_by_name(
            report_type_name,
            reporting_api.report_type_api.get_report_types(org_id).report_types,
        )
        new_report = Report(
            category_id=category_id,
            icon=icon,
            name=report_name,
            type_id=report_type_id,
            report_data_type="JSON",
            report_data=report_data,
        )
        created_report: Report = reporting_api.report_api.create_report(
            organization_id=org_id, report=new_report
        )
        return created_report.id
    else:
        report_to_update = Report(report_data=report_data)
        reporting_api.report_api.update_report(
            organization_id=org_id, report_id=report_id, report=report_to_update
        )
        return report_id


def update_report_stream(
        api_key: str, org_id_or_name: str, report_id_or_name: str, report_data: dict
):
    reporting_api = ReportingApi(api_key)
    org_id = org_id_or_name
    organizations = reporting_api.organzation_api.get_organizations()
    if org_id_or_name not in organizations:
        org_id = find_item_id_by_name(org_id_or_name, organizations)
        if org_id is None:
            raise RuntimeError(
                f"Unable to find organization with name {org_id_or_name}"
            )
    report_id = report_id_or_name
    reports = reporting_api.report_api.get_reports(organization_id=org_id).reports
    if report_id_or_name not in [report.id for report in reports]:
        report_id = find_item_id_by_name(
            report_id_or_name,
            reports,
        )
        if report_id is None:
            raise RuntimeError(f"Unable to find report with name {report_id_or_name}")
    report_stream_payload = ReportStreamPayload(
        payload_type="JSON", json_payload=report_data
    )
    reporting_api.report_api.update_report_stream(
        organization_id=org_id,
        report_id=report_id,
        report_stream_payload=report_stream_payload,
    )
