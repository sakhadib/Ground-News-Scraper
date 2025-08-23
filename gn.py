import subprocess
import os
import time  # Importing time module for the delay

# Get the current directory of this script
current_dir = os.path.dirname(os.path.realpath(__file__))


gn_sources = [
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


# Command to activate the virtual environment
activate_command = '.venv/Scripts/activate'

# Loop over each URL in the list
# Open terminal, activate the virtual environment, and run the command
try:
    # Start the subprocess to open terminal, activate virtual environment, and run commands sequentially
    for url in gn_sources:
        subprocess.run(f'cd {current_dir} && python g.py "{url}"', shell=True)
        time.sleep(1)
        subprocess.run("git add .", shell=True)
        subprocess.run(f"git commit -m 'Fetch news article {url}'", shell=True)
        time.sleep(1)  # Add 1 second delay between each URL
except Exception as e:
    print(f"Error: {e}")

