import graphene
from tanrail_service.models import *
from tanrail_dto.dtos import *


class SettingsBuilder:

    def get_train_data(train_id):
        train = Train.objects.filter(train_id=train_id).first()
        data = TrainOutput(name = train.train_no, train_id = train.train_id)
        return data

    def get_coach_data(coach_id):
        coach = Coach.objects.filter(coach_id=coach_id).first()
        train = SettingsBuilder.get_train_data(coach.train.train_id)
        data = CoachOutput(name = coach.coach_no, train = train)
        return data
    
    def get_main_activity_data(main_activity_id):
        main_activity_queryset = MainActivity.objects.filter(main_activity_id=main_activity_id).first()
        data = MainActivityOutput(name = main_activity_queryset.name, main_activity_id=main_activity_queryset.main_activity_id)
        return data
    
    def get_sub_activity_data(sub_activity_id):
        sub_activity_queryset = SubActivity.objects.filter(sub_activity_id=sub_activity_id).first()
        main_activity_data = SettingsBuilder.get_main_activity_data(sub_activity_queryset.main_activity.main_activity_id)
        data = SubActivityOutput(name = sub_activity_queryset.name, main_activity=main_activity_data)
        return data
    
    def get_sub_sub_activity_data(sub_sub_activity_id):
        sub_sub_activity_queryset = SubSubActivity.objects.filter(sub_sub_activity_id=sub_sub_activity_id).first()
        sub_activity_data = SettingsBuilder.get_sub_activity_data(sub_sub_activity_queryset.sub_activity.sub_activity_id)
        data = SubSubActivityOutput(name = sub_sub_activity_queryset.name, sub_activity=sub_activity_data)
        return data
    
    def get_actvities_done_details(activity_done_id):
        activity_done = ActivityDone.objects.filter(activity_done_id = activity_done_id).first()
        # print(activity_done)
        print(activity_done.sub_sub_activity)
        if activity_done.sub_activity is not None:
            subactivity = SubActivity.objects.filter(sub_activity_id = activity_done.sub_activity.sub_activity_id).first()
            subactivity_data = SettingsBuilder.get_sub_activity_data(subactivity.sub_activity_id)
            data = SubActivityDoneOutput(
                sub_activity = subactivity_data if activity_done.sub_activity else None,
                route1 = activity_done.route1,
                route2 = activity_done.route2,
                route3 = activity_done.route3,
                route4 = activity_done.route4,
                remarks = activity_done.remarks,
            )
            return data
        if activity_done.sub_sub_activity is not None:
            sub_sub_activity = SubSubActivity.objects.filter(sub_sub_activity_id = activity_done.sub_sub_activity.sub_sub_activity_id).first()
            sub_sub_activity_data = SettingsBuilder.get_sub_sub_activity_data(sub_sub_activity.sub_sub_activity_id)
            data = SubSubActivityDoneOutput(
                sub_sub_activity = sub_sub_activity_data if activity_done.sub_sub_activity else None,
                route1 = activity_done.route1,
                route2 = activity_done.route2,
                route3 = activity_done.route3,
                route4 = activity_done.route4,
                remarks = activity_done.remarks,
            )
            return data

    def get_report_details(report_id):
        report = Report.objects.filter(report_id=report_id).first()
        coach = SettingsBuilder.get_coach_data(report.coach.coach_id)
        return ReportOutput(
            coach = coach,
            coordinator_remarks = report.coordinator_remarks,
            supervisor_remarks = report.supervisor_remarks,
            created_at = report.created_at,
        )

    def get_all_report_related_details(report_id):
        report = Report.objects.filter(report_id = report_id).first()
        report_data = SettingsBuilder.get_report_details(report.report_id)
        report_activities_queryset = ReportForActivity.objects.filter(report = report)
        report_sub_activities_data = []
        report_sub_sub_activities_data = []

        activities_data = list(map(lambda query: SettingsBuilder.get_actvities_done_details(query.activity_done.activity_done_id), report_activities_queryset))
        
        for activity in activities_data:
            if isinstance(activity, SubActivityDoneOutput):
                report_sub_activities_data.append(activity)
            elif isinstance(activity, SubSubActivityDoneOutput):
                report_sub_sub_activities_data.append(activity)

        data = ReportDetails(
            report=report_data,
            report_sub_activities=report_sub_activities_data, 
            report_sub_sub_activities = report_sub_sub_activities_data,
            message = "Operation Successfull"
        )
        return data
        