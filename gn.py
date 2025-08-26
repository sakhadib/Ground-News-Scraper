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
    "https://ground.news/article/judge-blocks-trump-from-cutting-funding-from-34-cities-and-counties-over-sanctuary-policies_66ca03",
    "https://ground.news/article/ghislaine-maxwell-says-she-never-saw-trump-or-clinton-act-inappropriately-denies-client-list-in-doj-transcripts_5fce37",
    "https://ground.news/article/texas-lawmakers-give-final-approval-to-trump-backed-election-map-sending-it-to-governor_1e3655",
    "https://ground.news/article/india-says-us-trade-negotiations-are-still-going-on-as-fresh-tariffs-loom_835031",
    "https://ground.news/article/mamdanis-fundraising-surges-past-cuomo-adams-in-new-york-mayoral-race_8dd7f4",
    "https://ground.news/article/monitor-visits-jails-in-georgias-fulton-county-and-finds-safety-risks-due-to-understaffing",
    "https://ground.news/article/new-opm-director-estimates-300-000-federal-job-cuts-this-year-no-plans-to-relocate-jobs-from-dc",
    "https://ground.news/article/texas-lawmakers-give-final-approval-to-trump-backed-election-map-sending-it-to-governor_1e3655",
    "https://ground.news/article/trump-administration-halts-offshore-wind-project-in-rhode-island",
    "https://ground.news/article/pennsylvania-says-it-wont-give-voters-ssns-drivers-license-numbers-to-us-doj_2df31f",
    "https://ground.news/article/judge-blocks-trump-from-cutting-funding-from-34-cities-and-counties-over-sanctuary-policies_66ca03",
    "https://ground.news/article/mail-services-halt-us-deliveries-amid-tariff-rate-confusion_5cdeff",
    "https://ground.news/article/trumps-tariffs-could-reduce-us-deficit-by-4-trillion-cbo-estimates",
    "https://ground.news/article/russia-does-not-want-to-end-the-war-they-are-doing-everything-to-prevent-trump-from-imposing-sanctions-on-them",
    "https://ground.news/article/consumer-watchdog-ends-investigation-into-buy-now-pay-later-company-linked-to-donald-trump-jr_5a448e",
    "https://ground.news/article/body-cam-footage-shows-milwaukee-judge-denying-she-hid-an-immigrant-wanted-by-ice",
    "https://ground.news/article/california-gov-gavin-newsoms-national-profile-soars-with-latest-trump-fight-but-there-are-risks_2c3d6b",
    "https://ground.news/article/alaska-medical-board-approves-draft-to-discipline-providers-of-gender-affirming-care-for-youth",
    "https://ground.news/article/trump-white-house-personnel-honcho-sergio-gor-picked-as-ambassador-to-india-after-post-reporting-on-musk-feud-vetting-controversy",
    "https://ground.news/article/hhs-moves-to-strip-thousands-of-federal-health-workers-of-union-rights",
    "https://ground.news/article/trump-says-us-will-impose-tariffs-on-all-foreign-furniture_dbfe93",
    "https://ground.news/article/michael-faulkender-us-treasury-departments-no-2-official-set-to-depart-wsj-reports_f463ef",
    "https://ground.news/article/michael-faulkender-us-treasury-departments-no-2-official-set-to-depart-wsj-reports_f463ef",
    "https://ground.news/article/desantis-responds-to-alligator-alcatraz-ruling-touts-deportation-depot",
    "https://ground.news/article/trump-administration-says-grants-for-hispanic-serving-colleges-are-unconstitutional-and-it-wont-defend-them-in-court",
    "https://ground.news/article/missouri-gop-leader-says-lawmakers-will-start-with-a-congressional-map-drawn-in-dc",
    "https://ground.news/article/trump-says-hell-keep-extending-tiktok-shutdown-deadline_4e9222",
    "https://ground.news/article/texas-republicans-aim-for-final-passage-of-redistricting-after-california-democrats-counterpunch",
    "https://ground.news/article/trump-says-putin-may-come-to-world-cup",
    "https://ground.news/article/russia-does-not-want-to-end-the-war-they-are-doing-everything-to-prevent-trump-from-imposing-sanctions-on-them",
    "https://ground.news/article/putin-said-after-alaska-summit-on-improving-relations-with-the-united-states",
    "https://ground.news/article/us-raid-in-northern-syria-kills-senior-isis-financier",
    "https://ground.news/article/jd-vance-told-volodymyr-zelensky-to-behave-during-oval-office-meeting",
    "https://ground.news/article/sen-wicker-sen-fischer-depart-for-taiwan-indo-pacific-trip",
    "https://ground.news/article/trump-white-house-personnel-honcho-sergio-gor-picked-as-ambassador-to-india-after-post-reporting-on-musk-feud-vetting-controversy",
    "https://ground.news/article/un-backed-hunger-monitor-declares-famine-in-gaza-city-warns-of-rapid-spread_1cad26",
    "https://ground.news/article/25-people-killed-in-gaza-as-gaza-city-becomes-the-focus-of-famine-and-a-military-offensive_b881ca",
    "https://ground.news/article/dutch-foreign-minister-resigns-after-failing-to-secure-sanctions-against-israel_8a9eeb",
    "https://ground.news/article/25-people-killed-in-gaza-as-gaza-city-becomes-the-focus-of-famine-and-a-military-offensive_b881ca",
    "https://ground.news/article/dutch-foreign-minister-resigns-after-failing-to-secure-sanctions-against-israel_8a9eeb"
]

gn_new = [
    "https://ground.news/article/israel-airstrike-hits-gaza-hospital-killing-at-least-15-including-journalists-palestinian-officials-say_ec3bf9",
    "https://ground.news/article/kilmar-abrego-garcia-taken-into-ice-custody-in-baltimore-faces-possible-deportation-to-uganda_24c14f",
    "https://ground.news/article/advocates-warn-federal-budget-cuts-could-reduce-diversity-and-inclusion-initiatives",
    "https://ground.news/article/french-police-hold-suspect-after-bodies-of-four-men-found-in-river-seine",
    "https://ground.news/article/myanmar-junta-says-historic-railway-bridge-bombed-destroyed",
    "https://ground.news/article/patriotic-flag-raisers-attacked-with-petrol-bombs-after-hanging-st-georges-crosses-in-community-but-they-say-it-wont-stop-us",
    "https://ground.news/article/ukrainian-war-veterans-complete-bosphorus-swim-to-raise-prosthetic-funds",
    "https://ground.news/article/first-nations-partnership-to-buy-bc-port-terminal-that-moves-critical-minerals",
    "https://ground.news/article/american-accused-of-offering-sensitive-information-on-us-military-to-china-indicted-in-germany",
    "https://ground.news/article/expect-health-insurance-prices-to-rise-next-year-brokers-and-experts-say",
    "https://ground.news/article/israel-says-its-forces-will-withdraw-from-all-five-positions-in-southern-lebanon-in-stages-if-lebanon-disarms-hezbollah",
    "https://ground.news/article/indonesia-hosts-annual-us-led-combat-drills-with-indo-pacific-allies_76a186",
    "https://ground.news/article/cambodia-mps-pass-law-allowing-stripping-of-citizenship_ef045c",
    "https://ground.news/article/will-trump-put-money-over-principle-when-meeting-s-koreas-lee",
    "https://ground.news/article/irish-folk-band-the-mary-wallopers-say-they-were-muted-at-festival-for-showing-palestinian-flag-on-stage"
]


# Command to activate the virtual environment
activate_command = '.venv/Scripts/activate'

# Loop over each URL in the list
# Open terminal, activate the virtual environment, and run the command
try:
    # Start the subprocess to open terminal, activate virtual environment, and run commands sequentially
    for url in gn_new:
        subprocess.run(f'cd {current_dir} && python g.py "{url}"', shell=True)
        time.sleep(1)
        subprocess.run("git add .", shell=True)
        subprocess.run(f"git commit -m \"Fetch news article {url}\"", shell=True)
        time.sleep(1)  # Add 1 second delay between each URL
except Exception as e:
    print(f"Error: {e}")

