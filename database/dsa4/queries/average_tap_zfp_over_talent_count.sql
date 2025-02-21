SELECT
  t.talent_name AS talent,
  COUNT(*) AS talent_count,
  AVG(tr.tap_zfp) AS avg_tap_zfp,
  tc.talent_category_name AS category
FROM talents_rolls tr
JOIN talents t ON tr.talent_id = t.talent_id
JOIN talent_categories tc ON t.talent_category_id = tc.talent_category_id
WHERE tr.character_id = 1
GROUP BY t.talent_name, tc.talent_category_name;
