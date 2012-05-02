select 
	tbl_loot.loot_id,
	b.loot_id,
	cast(tbl_character.name as varchar(20)) as player, 
	cast(tbl_item.name as varchar(60)) as item, 
	tbl_loot.event_timestamp,
	b.event_timestamp,
	tbl_loot.submitter_user_id,
	b.submitter_user_id
from
	((tbl_loot inner join tbl_character on tbl_loot.character_id = tbl_character.character_id)
	inner join tbl_item on tbl_loot.item_id = tbl_item.item_id) 
	inner join tbl_loot b on (tbl_loot.item_id = b.item_id and tbl_loot.character_id = b.character_id)
where 
tbl_loot.submitter_user_id != b.submitter_user_id
and tbl_loot.event_timestamp != b.event_timestamp
and extract(hour from tbl_loot.event_timestamp) = extract(hour from b.event_timestamp)
and extract(day from tbl_loot.event_timestamp) = extract(day from b.event_timestamp)
and extract(month from tbl_loot.event_timestamp) = extract(month from b.event_timestamp)
and extract(year from tbl_loot.event_timestamp) = extract(year from b.event_timestamp)
and tbl_loot.event_timestamp > '2009-04-18 16:00:00'
;


select 
	count(*)
from
	((tbl_loot inner join tbl_character on tbl_loot.character_id = tbl_character.character_id)
	inner join tbl_item on tbl_loot.item_id = tbl_item.item_id) 
	inner join tbl_loot b on (tbl_loot.item_id = b.item_id and tbl_loot.character_id = b.character_id)
where 
tbl_loot.submitter_user_id != b.submitter_user_id
and tbl_loot.event_timestamp != b.event_timestamp
and extract(hour from tbl_loot.event_timestamp) = extract(hour from b.event_timestamp)
and extract(day from tbl_loot.event_timestamp) = extract(day from b.event_timestamp)
and extract(month from tbl_loot.event_timestamp) = extract(month from b.event_timestamp)
and extract(year from tbl_loot.event_timestamp) = extract(year from b.event_timestamp)
;


delete from tbl_loot where tbl_loot.loot_id in (select tbl_loot.loot_id from 
	((tbl_loot inner join tbl_character on tbl_loot.character_id = tbl_character.character_id)
	inner join tbl_item on tbl_loot.item_id = tbl_item.item_id) 
	inner join tbl_loot b on (tbl_loot.item_id = b.item_id and tbl_loot.character_id = b.character_id)
where 
tbl_loot.submitter_user_id != b.submitter_user_id
and tbl_loot.event_timestamp != b.event_timestamp
and extract(hour from tbl_loot.event_timestamp) = extract(hour from b.event_timestamp)
and extract(day from tbl_loot.event_timestamp) = extract(day from b.event_timestamp)
and extract(month from tbl_loot.event_timestamp) = extract(month from b.event_timestamp)
and extract(year from tbl_loot.event_timestamp) = extract(year from b.event_timestamp)
)
;

