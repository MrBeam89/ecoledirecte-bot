#    EcoleDirecte Bot (zip_source.py)
#    Copyright (C) 2023-2024 MrBeam89_
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program. If not, see <https://www.gnu.org/licenses/>.

import os
import tempfile
import git
import zipfile

from config import ECOLEDIRECTE_DIR

TEMP_DIR = tempfile.gettempdir() # Chemin d'accès du répertoire temporaire pour stocker l'archive

# Obtenir les noms de fichiers dans le dossier du bot (ignorer les autres répertoires)
filenames = []
for filename in os.listdir(ECOLEDIRECTE_DIR):
    if os.path.isfile(filename):
        filenames.append(filename)

# Obtenir les chemins d'accès à ignorer
repo = git.repo.base.Repo(ECOLEDIRECTE_DIR)
ignored_paths = repo.ignored(filenames)

def create_zip_source(zip_filename):
    # Stocker l'archive ZIP dans le répertoire temporaire
    zfile_filepath = os.path.join(TEMP_DIR, zip_filename)

    # Ne pas recréer l'archive si elle a déjà été créée
    if os.path.exists(zfile_filepath):
        return zfile_filepath

    # Créer l'archive ZIP
    zfile =  zipfile.ZipFile(zfile_filepath, 'w', zipfile.ZIP_DEFLATED)

    # Pour chaque fichier dans le répertoire du bot
    for filename in filenames:
        # Si le fichier est à ignorer, passer le reste de la boucle
        if filename in ignored_paths: continue

        # Ajouter le fichier à l'archive
        filepath = os.path.join(ECOLEDIRECTE_DIR, filename)
        zfile.write(filepath, filename)

    # Renvoyer le chemin d'accès de l'archive pour utilisation ultérieure
    return zfile_filepath
