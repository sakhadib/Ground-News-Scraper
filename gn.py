import subprocess
import os
import time  # Importing time module for the delay

# Get the current directory of this script
current_dir = os.path.dirname(os.path.realpath(__file__))


gn_sources = [
    ""
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

