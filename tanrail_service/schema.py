import graphene
from tanrail_dto.dtos import *
from.models import *
from tanrail_builder.builder import SettingsBuilder

class AllQuery(graphene.ObjectType):
    all_trains = graphene.List(TrainCoachOutput)
    report_data = graphene.Field(ReportDetails, report_id = graphene.UUID(required = True))

    @staticmethod
    def resolve_all_trains(self,info):
        try:
            trains = Train.objects.all()
            data = []
            for train in trains:
                coach = Coach.objects.filter(train = train).count()
                data.append(TrainCoachOutput(train_name = train.train_no, coach_no=coach))
            return data
        except Exception as e:
            print(e)
            return None
        
    @staticmethod
    def resolve_report_data(self, info, report_id):
        try:
            if report_id is not None:
                report_data = SettingsBuilder.get_all_report_related_details(report_id=report_id)
                return report_data
            return None
        except Exception as e:
            print(e)
            return None
            