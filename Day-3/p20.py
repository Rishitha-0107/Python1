def workshop_report(d1,d2, d3):
    d1_s=set(email.lower() for email in d1)
    d2_s=set(email.lower() for email in d2)
    d3_s=set(email.lower() for email in d3)
    tot_unique=d1_s| d2_s| d3_s
    all_three=d1_s&d2_s&d3_s
    only_d1=d1_s - d2_s - d3_s
    only_d2=d2_s - d1_s - d3_s
    only_d3=d3_s - d1_s - d2_s
    exactly_one_day=only_d1 | only_d2 | only_d3
    overlap_d1_d2=len(d1_s& d2_s)
    overlap_d2_d3=len(d2_s&d3_s)
    overlap_d1_d3=len(d1_s&d3_s)
    # Step 6: Final Report
    print("Workshop Attendance Report\n")
    print("unique attendees:",len(tot_unique))
    print("List of unique attendees:", sorted(tot_unique), "\n")
    print("Attendees who attended all three days:",len(all_three))
    print("List:",sorted(all_three),"\n")
    print("Attendees who attended exactly one day:",len(exactly_one_day))
    print("List:", sorted(exactly_one_day),"\n")
    print("Pairwise overlap counts:")
    print("Day1 & Day2:",overlap_d1_d2)
    print("Day2 & Day3:",overlap_d2_d3)
    print("Day1 & Day3:",overlap_d1_d3)
d1= ["rishi@gmail.com","rishi@outlook.com","Chrry@gmail.com","lucky@gmail.com"]
d2= ["sonu@gmail.com","dave@example.com","Chrry@gmail.com"]
d3 = ["lucky@gmail.com","charlie@example.com","Chrry@gmail.com","sonu@gmail.com"]
workshop_report(d1,d2,d3)