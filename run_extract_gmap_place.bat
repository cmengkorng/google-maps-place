@echo off
call .venv\Scripts\activate.bat
python main.py ^
  --keywords "Restaurant Food and Drink" "Hotel or Guesthouse" "Massage or Spa" "Resort Private" "Sport Club or Gym" "Hospitals" "School or University" ^
  --file scan_area_HORECA-KOH_RONG_AREA ^
  --outlet-check ^
  --outlet-file data/master/all_kb_outlets.xlsx