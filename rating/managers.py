from django.db import models

class VoteManager(models.Manager):
    r"""Custom manager to deal with counting votes."""
    use_for_related_fields = True
    
    def total(self, atom=None):
        r"""Returns the total votes for `atom`.  If atom is none return the total vote set."""
        if atom is not None:
            votes = self.filter(atom=atom)
        else:
            votes = self.all()
        return sum([v.vote for v in votes])

    def totalUp(self,atom=None):
        if atom is not None:
            votesUp = self.filter(atom=atom)
        else:
            votesUp = self.all()
        return sum([v.voteUp for v in votesUp])

    def totalDown(self,atom=None):
        if atom is not None:
            votesDown = self.filter(atom=atom)
        else:
            votesDown = self.all()
        return sum([v.voteDown for v in votesDown])