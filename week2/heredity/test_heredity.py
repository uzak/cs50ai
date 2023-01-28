# Author   : Martin Užák <uzak+git@mailbox.org>
# Creation : 2022-10-30 09:48

from heredity import *

people = {
'Harry': {'name': 'Harry', 'mother': 'Lily', 'father': 'James', 'trait': None},
'James': {'name': 'James', 'mother': None, 'father': None, 'trait': True},
'Lily': {'name': 'Lily', 'mother': None, 'father': None, 'trait': False}
}
one_gene = {"Harry"}
two_genes = {"James"}
have_trait = {"James"}

p = joint_probability(people, one_gene, two_genes, have_trait)
print(p)
