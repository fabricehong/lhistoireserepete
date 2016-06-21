# -*- coding: utf-8 -*-

urls = ["http://www.letemps.ch/sciences/2016/06/18/traversee-atlantique"
        "-bertrand-piccard",
        "http://www.letemps.ch/monde/2016/06/18/vaste-coup-filet-haute-tension-belgique",
        "http://www.letemps.ch/economie/2016/06/17/presidents-grands-groupes-suisses-mieux-payes-monde",
        "http://www.letemps.ch/economie/2016/06/17/suisse-va-reprendre-discussions-inde",
        "http://www.letemps.ch/monde/2016/06/17/politique-migratoire-honteuse-europe-aura-plus-aucune-credibilite",
        "http://www.letemps.ch/sport/2016/06/17/roumanie-albanie-stade-yverdon-euro",
        "https://www.letemps.ch/economie/2016/06/16/bns-ne-croit-brexit-s-y-prepare"]


def get_relations_by_id(id):
        """ Return a fake list of user recommended articles """
        return ["news$$" + url for url in urls]
