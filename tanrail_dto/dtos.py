import graphene

class createTrainAndCoach(graphene.InputObjectType):
    train_name = graphene.String()
    coach_no = graphene.Int()

class TrainCoachOutput(graphene.ObjectType):
    train_name = graphene.String()
    coach_no = graphene.Int()

class TrainOutput(graphene.ObjectType):
    name = graphene.String()
    train_id = graphene.UUID()

class CoachOutput(graphene.ObjectType):
    name = graphene.String()
    train = graphene.Field(TrainOutput)

class MainActivityOutput(graphene.ObjectType):
    main_activity_id = graphene.UUID()
    name = graphene.String()

class SubActivityInput(graphene.InputObjectType):
    name = graphene.String()
    main_activity_id = graphene.UUID() 

class SubActivityOutput(graphene.ObjectType):
    name = graphene.String()
    main_activity = graphene.Field(MainActivityOutput) 

class SubSubActivityInput(graphene.InputObjectType):
    name = graphene.String()
    sub_activity_id = graphene.UUID() 

class SubSubActivityOutput(graphene.ObjectType):
    name = graphene.String()
    sub_activity = graphene.Field(SubActivityOutput)

class ActivityDoneInput(graphene.InputObjectType):
    sub_activity = graphene.UUID()
    sub_sub_activity = graphene.UUID()
    route1 = graphene.String()
    route2 = graphene.String()
    route3 = graphene.String()
    route4 = graphene.String()
    remarks = graphene.String()

class SubActivityDoneOutput(graphene.ObjectType):
    sub_activity = graphene.Field(SubActivityOutput)
    route1 = graphene.String()
    route2 = graphene.String()
    route3 = graphene.String()
    route4 = graphene.String()
    remarks = graphene.String()

class SubSubActivityDoneOutput(graphene.ObjectType):
    sub_sub_activity = graphene.Field(SubSubActivityOutput)
    route1 = graphene.String()
    route2 = graphene.String()
    route3 = graphene.String()
    route4 = graphene.String()
    remarks = graphene.String()

class ReportInput(graphene.InputObjectType):
    coach = graphene.UUID()
    coordinator_remarks = graphene.String()
    supervisor_remarks = graphene.String()

class ReportOutput(graphene.ObjectType):
    coach = graphene.Field(CoachOutput)
    coordinator_remarks = graphene.String()
    supervisor_remarks = graphene.String()
    created_at = graphene.Date()

class ReportActivityInput(graphene.InputObjectType):
    activites = graphene.List(ActivityDoneInput)
    report = graphene.Field(ReportInput)

class ReportActivityOutput(graphene.ObjectType):
    activites = graphene.List(SubActivityDoneOutput)
    report = graphene.Field(ReportOutput)

class ReportRemarksInput(graphene.InputObjectType):
    report_id = graphene.UUID()
    supervisor_remarks = graphene.String()
    coordinator_remarks = graphene.String()

class ReportDetails(graphene.ObjectType):
    report = graphene.Field(ReportOutput)
    report_sub_activities = graphene.List(SubActivityDoneOutput)
    report_sub_sub_activities = graphene.List(SubSubActivityDoneOutput)
    message = graphene.String()