import subprocess
import os
import time  # Importing time module for the delay

# Get the current directory of this script
current_dir = os.path.dirname(os.path.realpath(__file__))


gn_sources = [
    "https://ground.news/article/thai-court-clears-ex-pm-thaksin-shinawatra-in-royal-insult-case-lawyer-says_f8c282",
    "https://ground.news/article/netanyahu-says-israel-to-begin-gaza-ceasefire-negotiations-to-end-war-release-hostages_9a880b",
    "https://ground.news/article/trump-administration-sanctions-icc-officials-for-efforts-to-arrest-americans-israelis_06e367",
    "https://ground.news/article/israel-has-begun-first-stages-of-its-planned-assault-on-gaza-city-says-israeli-military-spokesman_29669e",
    "https://ground.news/article/trump-white-house-personnel-honcho-sergio-gor-picked-as-ambassador-to-india-after-post-reporting-on-musk-feud-vetting-controversy",
    "https://ground.news/article/former-president-joseph-kabila-faces-death-penalty-for-war-crimes_9809ea",
    "https://ground.news/article/top-officials-of-amazon-nations-meet-in-colombia-to-push-joint-rainforest-protection-plan",
    "https://ground.news/article/former-sri-lankan-president-wickremesinghe-arrested-on-allegations-of-misusing-state-funds_31b6f9",
    "https://ground.news/article/canada-joins-call-to-protect-gaza-journalists-allow-foreign-media",
    "https://ground.news/article/germany-will-not-recognize-the-palestinian-state-anytime-soon_fa4616",
    "https://ground.news/article/israeli-militarys-own-data-indicates-civilian-death-rate-of-83-in-gaza-war_032e49",
    "https://ground.news/article/trump-says-intel-has-agreed-to-give-us-10-stake-in-chipmaker_307403",
    "https://ground.news/article/rajya-sabha-passes-online-gaming-bill-amid-opposition-protests",
    "https://ground.news/article/japanese-city-proposes-two-hour-daily-limit-for-smartphone-use_95fe80",
    "https://ground.news/article/after-promoting-boycott-measures-the-population-authority-blocked-the-entry-of-the-mayor-of-barcelona-to-israel",
    "https://ground.news/article/man-appears-in-court-over-palestine-action-raf-brize-norton-break-in_2f5cf6",
    "https://ground.news/article/trumps-tariffs-could-reduce-us-deficit-by-4-trillion-cbo-estimates",
    "https://ground.news/article/judge-blocks-trump-from-cutting-funding-from-34-cities-and-counties-over-sanctuary-policies_66ca03"
]


# Command to activate the virtual environment
activate_command = '.venv/Scripts/activate'

# Loop over each URL in the list
# Open terminal, activate the virtual environment, and run the command
try:
    # Start the subprocess to open terminal, activate virtual environment, and run commands sequentially
    for url in gn_sources:
        subprocess.run(f'cd {current_dir} && python g.py "{url}"', shell=True)
        time.sleep(1)  # Add 1 second delay between each URL
except Exception as e:
    print(f"Error: {e}")

