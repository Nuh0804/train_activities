from django.db import IntegrityError
import graphene
from tanrail_dto.dtos import *
from .models import *
# Create your views here.


class CreateTrainAndCoachMutation(graphene.Mutation):
    class Arguments:
        input = createTrainAndCoach(required = True)

    data = graphene.String()
    success = graphene.Boolean()

    @classmethod
    def mutate(cls, root, info, input):
        try:
            train = Train.objects.create(train_no = input.train_name)
            for number in range(1,input.coach_no+1):
                Coach.objects.create(coach_no = f"{train.train_no[0:2]}{number}", train = train)
            return CreateTrainAndCoachMutation(data = "Operation Successful", success = True)
        except Exception as e:
            return CreateTrainAndCoachMutation(data = str(e), success = False)
        

class MainActivityMutation(graphene.Mutation):
    class Arguments:
        name = graphene.String(required = True)

    data = graphene.String()
    success = graphene.Boolean()

    @classmethod
    def mutate(cls, root, info, name):
        try:
            MainActivity.objects.create(name=name)
            return MainActivityMutation(data = "Operation Successful", success = True)
        except Exception as e:
            print(e)
            return MainActivityMutation(data = str(e), success = False)
        

class SubActivityMutation(graphene.Mutation):
    class Arguments:
        input = SubActivityInput()

    data = graphene.String()
    success = graphene.Boolean()

    @classmethod
    def mutate(cls, root, info, input):
        try:
            main_activity = MainActivity.objects.filter(main_activity_id=input.main_activity_id).first()
            SubActivity.objects.create(name = input.name ,main_activity=main_activity)
            return MainActivityMutation(data = "Operation Successful", success = True)
        except MainActivity.DoesNotExist:
            return MainActivityMutation(data = "Not main Activity found", success = False)
        except IntegrityError as e:
            print(e)
            return MainActivityMutation(data = "Failed to create", success = False)
        except Exception as e:
            print(e)
            return MainActivityMutation(data = str(e), success = False)
        

class SubSubActivityMutation(graphene.Mutation):
    class Arguments:
        input = SubSubActivityInput()

    data = graphene.String()
    success = graphene.Boolean()

    @classmethod
    def mutate(cls, root, info, input):
        try:
            sub_activity = SubActivity.objects.filter(sub_activity_id=input.sub_activity_id).first()
            SubSubActivity.objects.create(name = input.name ,sub_activity=sub_activity)
            return SubSubActivityMutation(data = "Operation Successful", success = True)
        except SubActivity.DoesNotExist:
            return SubSubActivityMutation(data = "Not main Activity found", success = False)
        except IntegrityError as e:
            print(e)
            return SubSubActivityMutation(data = "Failed to create", success = False)
        except Exception as e:
            print(e)
            return SubSubActivityMutation(data = str(e), success = False)
        

class ReportMutation(graphene.Mutation):
    class Arguments:
        input = ReportActivityInput()
    
    data = graphene.String()
    success = graphene.Boolean()

    @classmethod
    def mutate(cls, root, info, input):
        try:
            coach = Coach.objects.filter(coach_id = input.report.coach).first()
            report = Report.objects.create(coach =coach)
            for activity in input.activites:
                if activity.sub_activity is not None:
                    sub_activity = SubActivity.objects.filter(sub_activity_id=activity.sub_activity).first()
                    activity_done = ActivityDone.objects.create(
                        sub_activity = sub_activity,
                        coach = coach,
                        route1 = activity.route1,
                        route2 = activity.route2,
                        route3 = activity.route3,
                        route4 = activity.route4,
                        remarks = activity.remarks,
                    )
                if activity.sub_sub_activity is not None:
                    print(activity.sub_sub_activity)
                    sub_sub_activity = SubSubActivity.objects.filter(sub_sub_activity_id = activity.sub_sub_activity).first()
                    print(sub_sub_activity)
                    activity_done = ActivityDone.objects.create(
                        sub_sub_activity = sub_sub_activity,
                        coach = coach,
                        route1 = activity.route1,
                        route2 = activity.route2,
                        route3 = activity.route3,
                        route4 = activity.route4,
                        remarks = activity.remarks,
                )
                ReportForActivity.objects.create(report = report, activity_done = activity_done)
            return ReportMutation(data = "Operation Successful", success = True)
        except Exception as e:
            print(e)
            return ReportMutation(data = str(e), success = False)
        
# class ReportRemarks(graphene.Mutation):
#     class Arguments:
#         input = ReportRemarksInput
    
#     data = graphene.String()
#     success = graphene.Boolean()

#     @classmethod
#     def mutate(cls, root, info, input):
#         try:
#             report = Report.objects.filter(report_id = input.report_id).first()

class Mutation(graphene.ObjectType):
    create_train_coach = CreateTrainAndCoachMutation.Field()
    create_activity = MainActivityMutation.Field()
    create_sub_activity = SubActivityMutation.Field()
    create_sub_sub_activity = SubSubActivityMutation.Field()
    create_report = ReportMutation.Field()