from pathlib import Path
from datetime import datetime
import pypdftk
import pandas as pd
from app.models import Entity


if __name__ == '__main__':
    # Declare paths to be used
    data_dir = Path("data/")
    output_dir = Path("output/")
    writeable_pdf = data_dir.joinpath("f2678.pdf")
    today = datetime.today().strftime('%Y-%m-%d')

    # Import excel data to dataframe
    df = pd.read_excel(data_dir.joinpath("data.xlsx"))

    # Declare incorrect datatype columns
    col_types = {"zipcode": str}
    df = df.astype(col_types)

    # declare static entity representing agent of record
    agent = Entity.from_dict(
        {
            "id": "1000",
            "fname": "Trusted",
            "lname": "Agent",
            "job": "Agent",
            "payrate": 30.00,
            "ssn": "012345678",
            "dob": "2001-01-01",
            "phone": "(012) 345-6789",
            "email": "trusted.agent@example.com",
            "address": "123 PEO Way",
            "city": "Anywhere",
            "state": "AZ",
            "zipcode": "01234"
        }
    )

    for idx, row in df.iterrows():
        # Declare form data using each row
        pdf_data = {
            # "c1_1[0]":        # Appoint
            "topmostSubform[0].Page1[0].c1_1[1]": "2",    # Revoke
            "topmostSubform[0].Page1[0].Form2678-EIN[0].f1_1[0]": row.ssn[:2],  # First 2 digits FEIN
            "topmostSubform[0].Page1[0].Form2678-EIN[0].f1_2[0]": (''.join(row.ssn.split('-')))[2:],   # last 7 digits FEIN
            "topmostSubform[0].Page1[0].f1_3[0]": f"{row.fname} {row.lname}",  # Employer/Payer name
            # "topmostSubform[0].Page1[0].f1_4[0]": # Trade Name
            "topmostSubform[0].Page1[0].f1_5[0]": row.address,
            "topmostSubform[0].Page1[0].f1_6[0]": row.city,
            "topmostSubform[0].Page1[0].f1_7[0]": row.state,
            "topmostSubform[0].Page1[0].f1_8[0]": f"0{row.zipcode}" if len(row.zipcode) < 5 else row.zipcode,
            # Foreign address block
            # "topmostSubform[0].Page1[0].f1_9[0]"
            # "topmostSubform[0].Page1[0].f1_10[0]"
            # "topmostSubform[0].Page1[0].f1_11[0]"
            # All Employees
            "topmostSubform[0].Page1[0].c1_2[0]": "Chck1",
            "topmostSubform[0].Page1[0].c1_4[0]": "Chck1",
            "topmostSubform[0].Page1[0].c1_6[0]": "Chck1",
            "topmostSubform[0].Page1[0].c1_8[0]": "Chck1",
            "topmostSubform[0].Page1[0].c1_10[0]": "Chck1",
            "topmostSubform[0].Page1[0].c1_12[0]": "Chck1", 
            "topmostSubform[0].Page1[0].c1_14[0]": "Chck1",
            # # Some Employees
            # "topmostSubform[0].Page1[0].c1_3[0]": "Chck2",
            # "topmostSubform[0].Page1[0].c1_5[0]": "Chck2",
            # "topmostSubform[0].Page1[0].c1_7[0]": "Chck2",
            # "topmostSubform[0].Page1[0].c1_9[0]": "Chck2",
            # "topmostSubform[0].Page1[0].c1_11[0]": "Chck2",
            # "topmostSubform[0].Page1[0].c1_13[0]": "Chck2",
            # "topmostSubform[0].Page1[0].c1_15[0]": "Chck2",
            # # HHCSR appointment for FUTA
            # "topmostSubform[0].Page1[0].c1_16[0]":
            "topmostSubform[0].Page1[0].f1_12[0]": f"{row.fname} {row.lname}",
            "topmostSubform[0].Page1[0].f1_13[0]": row.job,
            "topmostSubform[0].Page1[0].f1_14[0]": row.phone,
            # Page 2
            "topmostSubform[0].Page2[0].AgentEIN-No\\.[0].f2_1[0]": agent.ssn[:2],
            "topmostSubform[0].Page2[0].AgentEIN-No\\.[0].f2_2[0]": agent.ssn[2:],
            "topmostSubform[0].Page2[0].f2_3[0]": f"{agent.fname} {agent.lname}",
            # "topmostSubform[0].Page2[0].f2_4[0]"     # Trade Name
            "topmostSubform[0].Page2[0].f2_5[0]": agent.address,
            "topmostSubform[0].Page2[0].f2_6[0]": agent.city,
            "topmostSubform[0].Page2[0].f2_7[0]": agent.state,
            "topmostSubform[0].Page2[0].f2_8[0]": agent.zipcode,
            # # Foreign Address (Agent)
            # "topmostSubform[0].Page2[0].f2_9[0]"
            # "topmostSubform[0].Page2[0].f2_10[0]"
            # "topmostSubform[0].Page2[0].f2_11[0]"
            # # HHCSR Flag
            # "topmostSubform[0].Page2[0].c2_1[0]":
            "topmostSubform[0].Page2[0].f2_12[0]": f"{agent.fname} {agent.lname}",
            "topmostSubform[0].Page2[0].f2_13[0]": agent.job,
            "topmostSubform[0].Page2[0].f2_14[0]": agent.phone
        }
        print(pdf_data)

        output_file = output_dir.joinpath(f"{today}_{idx}_{row.lname}-{row.fname}.pdf")
        filled_pdf = pypdftk.fill_form(str(writeable_pdf), pdf_data, out_file=output_file)