# 📋 Instructions de migration de la documentation

## 🚀 Étapes de migration

1. **Exécuter le script de migration** :
   ```bash
   cd docs
   python migrate_docs.py
   ```

2. **Vérifier la structure** :
   ```bash
   tree /F
   ```

3. **Mettre à jour les liens internes** :
   - Tous les fichiers qui référencent d'autres documents doivent être mis à jour
   - Utiliser les nouveaux chemins avec dossiers

4. **Supprimer les anciens fichiers** :
   - Après vérification, supprimer les fichiers en MAJUSCULES restants

## 📁 Nouvelle structure

```
docs/
├── README.md                      # Conservé en majuscules
├── index.md                       # Renommé en minuscules
├── api/                          # Documentation API
├── architecture/                 # Architecture et conception
├── guides/                       # Guides techniques généraux
├── performance/                  # Performance et Green Code
├── security/                     # Sécurité et conformité
├── tests/                        # Documentation des tests
├── support/                      # Support et dépannage
├── postman/                      # Collections Postman existantes
├── developpement/                # Dossier existant conservé
└── green-code/                   # Dossier existant conservé
```

## ✅ Checklist post-migration

- [ ] Script exécuté sans erreur
- [ ] Tous les fichiers déplacés
- [ ] Liens internes mis à jour
- [ ] Navigation testée
- [ ] Anciens fichiers supprimés
- [ ] Commit des changements
