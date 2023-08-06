dict(
    flow1=[
        dict(
            type="CropStage",
            params=dict(
                crop_rect=[190, 5, 480, 320]
            )
        ),
        dict(
            type="DetectionStage",
            params=dict(
                draw=True
            )
        ),
        dict(
            type="RuleStage",
            params=dict(
                some_file="$YF_PROJ_PATH/project/assets/some_file.txt"
            )
        )
    ],

    # We can add more flows here
    # flow2 = [
    #     dict(
    #         type="SomeStage",
    #     ),
    #     dict(
    #         type="OtherStage",
    #     )
    # ]
)
