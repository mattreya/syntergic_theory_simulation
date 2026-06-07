#!/bin/bash

# Define paths
SAFE_WORKSPACE="/home/matt/Documents/vscode/Syntergic Theory/"
HERMES_DROP_ZONE="/home/matt/Documents/vscode/hermes_shared_workspace/Syntergic Theory/"

echo "Syncing safe workspace to Hermes Drop Zone..."

# Use rsync for a one-way mirror from SAFE_WORKSPACE to HERMES_DROP_ZONE.
# --archive: preserve permissions, times, symbolic links, etc.
# --delete: delete files in the drop zone that no longer exist in the safe workspace
# --exclude '.git/': protect our git history from being mirrored or modified by Hermes
# --exclude 'venv/': exclude the virtual environment as Hermes should have its own or install its own dependencies
rsync --archive --delete --verbose --exclude '.git/' --exclude 'venv/' "$SAFE_WORKSPACE" "$HERMES_DROP_ZONE"

echo "Sync complete! Hermes now has the latest context, but your original files remain isolated and safe."
