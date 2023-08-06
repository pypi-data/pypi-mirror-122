# Kia Remarketing Supply

## People
- Supervisor: Jung Park (jungpark@kiausa.com)
- Data Scientist: Jason Kim (jasonkim@kiausa.com) 
- Business Analyst: Michael Bautista (mbautista@kiausa.com)


## PowerBI Dashboard for Fleet

[Dashboard](https://teams.microsoft.com/l/entity/1c4340de-2a85-40e5-8eb0-4f295368978b/_djb2_msteams_prefix_951923316?context=%7B%22subEntityId%22%3Anull%2C%22channelId%22%3A%2219%3Aa29e8dfe9f5f413785d6ae14e55f29b8%40thread.tacv2%22%7D&groupId=1796b789-568c-4dd4-aff2-66236d119c2a&tenantId=5fed94a0-4129-44a0-b507-a83a5c9e6dac)
![](screenshots/fleet_dashboard.png)

---

## Automation
- The bash scripts for running the ./clean_jupyter_notebooks is found in ./bash_scripts
- Scheduled runs using crontab
  - The current inventory fleet predition simulates sold dates from today + 45 days on a daily basis as 7:10 am PST
  - The fleet model is scheduled to retrain every week at 8:05 am PST on Sundays

### crontab -l
> CRON_TZ=UTC
> 
> \* \* \* \* \* /bin/bash /home/kma62139/python_projects/kia_remarketing_supply/bash_scripts/send_queued_email.sh
> 
> 0 14 * * * /bin/bash /home/kma62139/python_projects/kia_remarketing_supply/bash_scripts/fleet_ci_predict_sim_sale_price.sh ;  mail -s "Kia Remarketing Supply: 2.0-jmk-predict_fleet_ci.ipynb" jasonkim@kiausa.com < /home/kma62139/python_projects/kia_remarketing_supply/logs/2.0-jmk-predict_fleet_ci.log tail -10
> 
> 5 15 * * 0 /bin/bash /home/kma62139/python_projects/kia_remarketing_supply/bash_scripts/fleet_train_model.sh ; mail -s "Kia Remarketing Supply: 1.0-jmk-fleet_training.ipynb" jasonkim@kiausa.com < /home/kma62139/python_projects/kia_remarketing_supply/logs/1.0-jmk-fleet_training.log tail -10
